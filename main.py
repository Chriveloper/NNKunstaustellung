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
    linie1 = LineString([punkt, wand.coords[0]])
    linie2 = LineString([punkt, wand.coords[1]])


guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)