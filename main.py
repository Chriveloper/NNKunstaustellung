
from jamico import plot_room, create_room
from shapely import Point, LineString, Polygon
import random
import matplotlib.pyplot as plt
import numpy as np

room = create_room(30, 30, 0.2, 15)

raumPolygon = room[2]
kunstwerkPunkte = room[1]
waendeLinien = room[0]

# print("Kunstausstellung:", kunstausstellung)
# print("Kunstwerke:", kunstwerke)
# print("Wände:", waende)


def kunstwerkPolygon(kunstwerk):
    sichtPolygon = raumPolygon
    kunstwerkPunkt = kunstwerk
    #for wand in waendeLinien:

def schatten(punkt, wand):
    linie1 = LineString([punkt, wand.coords[0]])
    linie2 = LineString([punkt, wand.coords[1]])


guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)

plot_room(room, guards)


walls = room[0]
art_pieces = room[1] 

print(walls[0])

def getVis(art_piece, wall):
    i = 0
    for x in walls:
        walls[i]
        i+= 1



def getSlope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines.")
    return (y2 - y1) / (x2 - x1)

def cutVis(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
art_vis = []

for x in art_pieces:
    art_vis.append(getVis(x, walls))
    
