import random
import matplotlib.pyplot as plt
import numpy as np
from shapely import Point, LineString, Polygon
from jamico import create_room, plot_room


room = create_room(15, 15, 0.2, 12)



guards = [Point(random.random() * 15, random.random() * 15) for i in range(4)]
plot_room(room, guards)