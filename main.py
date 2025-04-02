import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.validation import explain_validity
from jamico import create_room  # Assuming `create_room` is defined in `jamico`
from schatten import schatten
from dictionary import createDict  

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


dict_poly = createDict(visibility_polygons)
print("keys of dictionary:", dict_poly.keys())