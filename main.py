import random
import matplotlib.pyplot as plt
import numpy as np
from shapely import Point, LineString, Polygon
from jamico import create_room, plot_room
room = create_room(30, 30, 0.2, 15)

outer_room = room[2]
print(outer_room)

guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)