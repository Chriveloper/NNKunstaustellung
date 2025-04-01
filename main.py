
from jamico import guards, plot_room, create_room
from shapely import Point, LineString, Polygon
import random
import matplotlib.pyplot as plt
import numpy as np

room = create_room(30, 30, 0.2, 15)

outer_room = room[2]
print(outer_room)

guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)

plot_room(room, guards)

print(guards)
print(room[0])
print(room[1])

walls = room[0]
art_pieces = room[1] 



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
    
