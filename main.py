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


# def createDict(artworks, artworkViewAreas):
#     dictKunstwerke = {}
#     keys = [[]]
#     values = []
    
#     i = 0
#     for a in artworkViewAreas:
#         locKey = []
#         locValue
#         locKey[i] = true
#         locValue = a
#         j = 0 
#         for b in artworkViewAreas:
#             if a==b:
#                 continue
#             else:
#                     if locValue.intersects(b):
#                       locKey[j] = true
#                       locValue = a.intersection(b)
#             j += 1
#         i += 1
#         keys.append(locKey)


def createDict(Areas):
    result_dict = {}

    num_polygons = len(Areas)

    # Iterate through all possible intersection combinations
    for i in range(1, 2**num_polygons):  # Avoid empty set (i=0)
        intersection = None
        locKey = [False] * num_polygons  # Initialize key with all False

        for j in range(num_polygons):
            if i & (1 << j):  # Check if polygon j is in this combination
                if intersection is None:
                    intersection = Areas[j]  # Start with first selected polygon
                else:
                    intersection = intersection.intersection(Areas[j])  # Intersect with next
                
                locKey[j] = True  # Mark polygon as included

        # Store the intersection polygon only if it's valid (not empty)
        if intersection and not intersection.is_empty:
            result_dict[tuple(locKey)] = intersection

    return result_dict

# Example polygons
polygon1 = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])  # Square
polygon2 = Polygon([(2, 2), (6, 2), (6, 6), (2, 6)])  # Overlaps with polygon1
polygon3 = Polygon([(5, 5), (7, 5), (7, 7), (5, 7)])  # Overlaps with polygon2
# create another list of example polygons
polygon4 = Polygon([(8, 8), (10, 8), (10, 10), (8, 10)])  # No overlap
# five more
polygon5 = Polygon([(12, 12), (14, 12), (14, 14), (12, 14)])  # No overlap
polygon6 = Polygon([(15, 15), (17, 15), (17, 17), (15, 17)])  # No overlap
# more
polygon7 = Polygon([(18, 18), (20, 18), (20, 20), (18, 20)])  # No overlap
polygon8 = Polygon([(22, 22), (24, 22), (24, 24), (22, 24)])  # No overlap

Areas = [polygon1, polygon2, polygon3, polygon4, polygon5, polygon6, polygon7, polygon8]



print(createDict(Areas))