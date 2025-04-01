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


def get_intersection(startPoint, endPoint, polygon, extensionStep=10, maxIterations=100):
    line = LineString([startPoint, endPoint])
    vector




guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)


def getSlope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines.")
    return (y2 - y1) / (x2 - x1)