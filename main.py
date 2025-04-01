import random
import matplotlib.pyplot as plt
import numpy as np
from shapely import Point, LineString, Polygon
from jamico import create_room, plot_room


room = create_room(30, 30, 0.2, 15)

raumPolygon = room[2]
kunstwerkPunkte = room[1]
waendeLinien = room[0]

print("Raum Polygon:", raumPolygon)
print("Kunstwerk Punkte:", kunstwerkPunkte)
print("Wände Linien:", waendeLinien)


def kunstwerkPolygon(kunstwerk):
    sichtPolygon = raumPolygon
    kunstwerkPunkt = kunstwerk
    for wand in waendeLinien:
        return null

def schatten(punkt, wand):
    line1 = LineString(punkt, wand.coords[0])
    line2 = LineString(punkt, wand.coords[1])


def getScaledVector(line):
    startPoint = line.coords[0]
    endPoint = line.coords[1]
    vector = (endPoint[0] - startPoint[0], endPoint[0] - startPoint[1])


guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)


def getSlope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines.")
    return (y2 - y1) / (x2 - x1)



# removing shaddows from the polygon
def removeShaddows(polygon_a, shaddows):
    for shadow in shaddows:
        polygon_a = polygon_a.difference(shadow)
    return polygon_a



arrKunstwerke = ["a", "b", "c", "d", "e", "f", "g", "h"]
# create an array with random polygons for each kunstwerk inside a 30x30 room nammed arrView
arrViews = []
for i in range(len(arrKunstwerke)):
    arrViews.append(Polygon([Point(random.random() * 15, random.random() * 15) for j in range(4)]))


# def createDict(artworks, artworkViewAreas):
#     dictKunstwerke = {}
#     keys = [[]]
#     values = []
    
#     i = 0
#     for a in artworkViewAreas:
#         locKey = []
#         locValue
#         locKey[i] = true
#         j = 0 
#         for b in artworkViewAreas:
#             if a==b:
#                 continue
#             else:
#                     locKey[a.intersects(b)] 
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

Areas = [polygon1, polygon2, polygon3]



print(createDict(arrViews))