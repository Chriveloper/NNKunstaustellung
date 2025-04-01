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
arrView = []
for i in range(len(arrKunstwerke)):
    arrView.append(Polygon([Point(random.random() * 15, random.random() * 15) for j in range(4)]))


def createDict(arrKunstwerke, arrView):
    # create a dict with the keys as boolean value array of intersection from a kunstwerk and the values as the intersection of the polygons from the kunstwerk view
    dictKunstwerke = {}
    for i in range(len(arrKunstwerke)):
        dictKunstwerke[arrKunstwerke[i]] = arrView[i]
    return dictKunstwerke
    

        
