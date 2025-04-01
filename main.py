import random
import matplotlib.pyplot as plt
import numpy as np
from shapely import Point, LineString, Polygon
from jamico import create_room, plot_room


room = create_room(30, 30, 0.2, 15)

raumPolygon = room[2]
kunstwerkPunkte = room[1]
waendeLinien = room[0]

print("Kunstausstellung:", kunstausstellung)
print("Kunstwerke:", kunstwerke)
# print("Wände:", waende)


def kunstwerkPolygon(kunstwerk):
    sichtPolygon = raumPolygon
    kunstwerkPunkt = kunstwerk
    for wand in waendeLinien:

def schatten(punkt, wand):


def get_intersection(startPoint, endPoint, polygon):
    line = LineString([startPoint, endPoint])
    # get vector of the line
    vector = (endPoint[0] - startPoint[0], endPoint[0] - startPoint[0])
    ray = line
    # keep extending the ray end until it hits the polygon
    while True:
        extendedRay = LineString([ray.coords[0], (ray.coords[1][0] + vector[0], ray.coords[1][1] + vector[1])])
        intersection = extendedRay.intersection(polygon)
        if intersection.is_empty:
            ray = extendedRay
        else:
            # return the intersection a bit further from the intersection added vector
            return Point(intersection.coords[0][0] + vector[0], intersection.coords[0][1] + vector[1])


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
arrView = []
for i in range(len(arrKunstwerke)):
    arrView.append(Polygon([Point(random.random() * 15, random.random() * 15) for j in range(4)]))


def createDict(arrKunstwerke, arrView):
    # create a dict with the keys as boolean value array of intersection from a kunstwerk and the values as the intersection of the polygons from the kunstwerk view
    dictKunstwerke = {}
    for i in range(len(arrKunstwerke)):
        dictKunstwerke[arrKunstwerke[i]] = arrView[i]
    return dictKunstwerke
    

        
