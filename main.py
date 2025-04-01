from jamico import room, guards, plot_room
from shapely import Point, LineString, Polygon


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
    