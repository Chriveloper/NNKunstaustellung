import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.validation import explain_validity
from jamico import create_poly_room  # use poly room version
from schatten import schatten
from dictionary import createDict
from scipo import find_best_combination
from guard import setGuard
from interface import get_polygon

drawVisLines = True  

# Use an interactive polygon.
user_polygon = get_polygon()
if user_polygon is None:
    raise SystemExit("No valid polygon was drawn.")

# Generate the room using the user polygon.
room = create_poly_room(user_polygon, wall_density=0.2, art_piece_number=5)
# In our poly room, the room boundary is the user polygon.
raumPolygon, kunstwerkPunkte, waendeLinien = room[2], room[1], room[0]

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

visibility_polygons = [
    kunstwerkPolygon(kunstwerk, raumPolygon, waendeLinien) for kunstwerk in kunstwerkPunkte
]



# Generate a list of unique colors for the polygons
colors = list(mcolors.TABLEAU_COLORS.values())
while len(colors) < len(kunstwerkPunkte):
    colors.extend(colors)  # repeat colors if necessary

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

# Plot the generated walls
for wall in waendeLinien:
    x, y = wall.xy
    plt.plot(x, y, color='black', linewidth=1)

# Plot the room boundary (user polygon)
x, y = raumPolygon.exterior.xy
plt.plot(x, y, color='blue', linewidth=1)



dict_poly = createDict(visibility_polygons)
guardPolys = find_best_combination(list(dict_poly.keys()))

print("guard poly: ", guardPolys)

# plot the guards
for guardPoly in guardPolys:
    guard = setGuard(dict_poly[list(dict_poly.keys())[guardPoly]])
    plt.plot(guard.x, guard.y, 'ko')  # Black for guards
    if drawVisLines:
        for kunstwerk in kunstwerkPunkte:
                line = LineString([guard, kunstwerk])
                if not any(line.intersects(wall) for wall in waendeLinien):
                    x, y = line.xy
                    plt.plot(x, y, color='red', alpha=0.3)




# Optionally draw lines of sight from guards to art pieces

        



# Set plot properties and display
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()