import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.validation import explain_validity
from jamico import create_room  # Assuming `create_room` is defined in `jamico`

# Create the room and extract its components
room = create_room(20, 20, 0.2, 5)
raumPolygon, kunstwerkPunkte, waendeLinien = room[2], room[1], room[0]

# print("Raum Polygon:", raumPolygon)
# print("Kunstwerk Punkte:", kunstwerkPunkte)
# print("Wände Linien:", waendeLinien)

# Function to calculate the visibility polygon for a given art piece
def kunstwerkPolygon(kunstwerk, raumPolygon, waendeLinien):
    sichtPolygon = raumPolygon
    schattenListe = []
    for wand in waendeLinien:
        shadow = schatten(kunstwerk, wand)
        if shadow is not None:
            schattenListe.append(shadow)
    return removeShadows(sichtPolygon, schattenListe)

# Function to calculate the shadow polygon for a given point and wall
def schatten(punkt, wand):
    line1 = LineString([punkt, wand.coords[0]])
    line2 = LineString([punkt, wand.coords[1]])
    extendedPoint1 = (
        wand.coords[0][0] + getScaledVector(line1)[0],
        wand.coords[0][1] + getScaledVector(line1)[1],
    )
    extendedPoint2 = (
        wand.coords[1][0] + getScaledVector(line2)[0],
        wand.coords[1][1] + getScaledVector(line2)[1],
    )
    polygon = Polygon([wand.coords[0], wand.coords[1], extendedPoint2, extendedPoint1])
    if not polygon.is_valid:
        print("Invalid shadow polygon:", explain_validity(polygon))
        return None
    return polygon

# Function to scale a vector by a fixed factor
def getScaledVector(line):
    scaleFactor = 1000  # Extend the vector by a large fixed factor
    startPoint, endPoint = line.coords[0], line.coords[1]
    vector = (endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])
    vectorLength = np.sqrt(vector[0]**2 + vector[1]**2)
    if vectorLength > 0:
        return (vector[0] * scaleFactor / vectorLength, vector[1] * scaleFactor / vectorLength)
    return (0, 0)  # Return zero vector if the length is zero

# Function to remove shadows from the visibility polygon
def removeShadows(polygon_a, shadows):
    if not polygon_a.is_valid:
        print("Invalid polygon_a:", explain_validity(polygon_a))
        return polygon_a
    for shadow in shadows:
        if shadow is None or not shadow.is_valid:
            continue
        polygon_a = polygon_a.difference(shadow)
    return polygon_a

# Generate random guards and art piece visibility polygons
guards = [Point(random.random() * 15, random.random() * 15) for _ in range(4)]
visibility_polygons = [
    kunstwerkPolygon(kunstwerk, raumPolygon, waendeLinien) for kunstwerk in kunstwerkPunkte
]

# Generate a list of unique colors for the polygons
colors = list(mcolors.TABLEAU_COLORS.values())
while len(colors) < len(kunstwerkPunkte):
    colors.extend(colors)  # Repeat colors if necessary

# Plot the visibility polygons, art pieces, walls, and guards
for i, vis_poly in enumerate(visibility_polygons):
    color = colors[i % len(colors)]
    if isinstance(vis_poly, MultiPolygon):
        for poly in vis_poly.geoms:
            x, y = poly.exterior.xy
            plt.fill(x, y, alpha=0.2, color=color)
    elif isinstance(vis_poly, Polygon):
        x, y = vis_poly.exterior.xy
        plt.fill(x, y, alpha=0.2, color=color)

    # Plot the corresponding art piece
    kunstwerk = kunstwerkPunkte[i]
    plt.plot(kunstwerk.x, kunstwerk.y, 'o', color=color)

# Plot the room walls
for wall in waendeLinien:
    x, y = wall.xy
    plt.plot(x, y, color='black', linewidth=1)

# Plot the room boundary
x, y = raumPolygon.exterior.xy
plt.plot(x, y, color='blue', linewidth=1)

# Plot the guards
for guard in guards:
    plt.plot(guard.x, guard.y, 'ko')  # Black for guards

# Set plot properties and display
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()

def create_artwork_visibility_dict(room, vis_polygons):
    """
    Create a dictionary mapping each boolean tuple (of length n, where n is the number of artworks)
    to a polygon. For each artwork:
      - If the boolean is True, its visibility polygon is intersected.
      - If False, its visibility polygon is subtracted.
    
    This results in 2^n entries describing the regions where certain artworks are "visible" (inside the polygon)
    and others are not.
    
    Args:
        room (Polygon): The entire room polygon.
        vis_polygons (list[Polygon]): A list of visibility polygons produced by kunstwerkPolygon().
    
    Returns:
        dict: Mapping of boolean tuples to resulting Polygons.
    """
    from itertools import product
    result = {}
    n = len(vis_polygons)
    for comb in product([True, False], repeat=n):
        region = room
        for i, flag in enumerate(comb):
            if flag:
                region = region.intersection(vis_polygons[i])
            else:
                region = region.difference(vis_polygons[i])
        result[comb] = region
    return result

# Example usage:
artwork_visibility_dict = create_artwork_visibility_dict(raumPolygon, visibility_polygons)
print(artwork_visibility_dict)