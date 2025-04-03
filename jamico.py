import random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, LineString, Polygon

def create_poly_room(user_polygon, wall_density, art_piece_number):
    """
    Generate a room from a user-supplied polygon.
    - Create art pieces randomly placed inside the polygon.
    - Store the polygon's boundary edges as walls.
    - Optionally generate additional internal walls by sampling a fixed-length segment
      that lies entirely within the polygon and does not cross any existing wall.
    """
    # Create art pieces inside the user_polygon.
    minx, miny, maxx, maxy = user_polygon.bounds
    art_pieces = []
    while len(art_pieces) < art_piece_number:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if user_polygon.contains(p):
            art_pieces.append(p)
    
    walls = []
    # Store the boundary edges of the polygon as walls
    exterior_coords = list(user_polygon.exterior.coords)
    for i in range(len(exterior_coords) - 1):
        wall = LineString([exterior_coords[i], exterior_coords[i + 1]])
        walls.append(wall)
    
    # Generate additional internal walls.
    max_attempts = int(wall_density * 200)
    attempts = 0

    # Diagonal of the polygon's bounding box used as a scale reference
    diag = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)

    while attempts < max_attempts:
        # Pick a random starting point strictly inside the polygon.
        pt1 = None
        while pt1 is None:
            candidate = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if user_polygon.contains(candidate):
                pt1 = candidate
        # Choose a random angle.
        angle = random.uniform(0, 2 * np.pi)
        # Choose a random wall length between 5% and 30% of the diagonal.
        random_length = random.uniform(0.05 * diag, 0.3 * diag)
        pt2 = Point(pt1.x + random_length * np.cos(angle), pt1.y + random_length * np.sin(angle))
        candidate_wall = LineString([pt1, pt2])
        
        # Accept candidate only if the entire segment lies within the polygon.
        if not user_polygon.contains(candidate_wall):
            attempts += 1
            continue
        
        # Ensure candidate wall does not properly cross any existing wall.
        valid = True
        # for wall in walls:
        #     if candidate_wall.crosses(wall):
        #         valid = False
        #         break
        
        if valid:
            walls.append(candidate_wall)
        attempts += 1

    return (walls, art_pieces, user_polygon)

def create_RecRoom(x_length, y_length, wall_density, art_piece_number):
    # add art pieces in random locations
    art_pieces = [Point(random.random() * x_length, random.random() * y_length) for i in range(art_piece_number)]

    walls = []
    # add vertical walls
    for x_temp in range(x_length - 1):
        x = x_temp + 1
        for y in range(y_length):
            if random.random() < wall_density:
                walls.append(LineString([(x, y), (x, y + 1)]))
    # add horizontal walls:
    for x in range(x_length):
        for y_temp in range(y_length - 1):
            y = y_temp + 1
            if random.random() < wall_density:
                walls.append(LineString([(x, y), (x + 1, y)]))

    # add outer borders:
    walls.append(LineString([(0, 0), (x_length, 0)]))
    walls.append(LineString([(0, 0), (0, y_length)]))
    walls.append(LineString([(x_length, 0), (x_length, y_length)]))
    walls.append(LineString([(0, y_length), (x_length, y_length)]))

    outer_room = Polygon([(0, 0), (x_length, 0), (x_length, y_length), (0, y_length)])

    return (walls, art_pieces, outer_room)




# # Imprecise ray casting algorithm, but probably the best approach here
# def visibility_polygon(p, walls, num_rays=1000, N=10000):
#     first_intersections = dict()
#     angles = np.linspace(0, 2*np.pi, num_rays)
#     for angle in angles:
#         q = Point(p.x + np.cos(angle) * N, p.y + np.sin(angle) * N)
#         ray = LineString([p, q])
#         all_intersections = {ray.intersection(wall): wall for wall in walls if ray.intersects(wall)}
#         closest_intersection = min(all_intersections.keys(), key=lambda r: p.distance(r))
#         first_intersections[angle] = (closest_intersection, all_intersections[closest_intersection])
#     polygon_vertices = []
#     for i in range(num_rays):
#         if first_intersections[angles[i]][1] != first_intersections[angles[i - 1]][1] or \
#            first_intersections[angles[i]][1] != first_intersections[angles[(i + 1) % num_rays]][1]:
#             polygon_vertices.append(first_intersections[angles[i]][0])
#     return Polygon(polygon_vertices)

# def plot_room(room, guards, lines_of_sight=True, vis_polygons=False):
#     walls, art_pieces, *outer_room = room

#     # Scatterplot for art pieces
#     x = [art_piece.x for art_piece in art_pieces]
#     y = [art_piece.y for art_piece in art_pieces]
#     plt.scatter(x, y, color="blue")

#     # Scatterplot for guards
#     x = [guard.x for guard in guards]
#     y = [guard.y for guard in guards]
#     plt.scatter(x, y, color="red")

#     # Draw walls
#     for wall in walls:
#         x, y = wall.xy
#         plt.plot(x, y, color='black')
#     plt.xticks([])
#     plt.yticks([])
#     plt.xlabel('')
#     plt.ylabel('')

#     # Optionally draw lines of sight from guards to art pieces
#     if lines_of_sight:
#         for guard in guards:
#             for art_piece in art_pieces:
#                 line = LineString([guard, art_piece])
#                 if not any(line.intersects(wall) for wall in walls):
#                     x, y = line.xy
#                     plt.plot(x, y, color='red', alpha=0.3)
    
#     # Optionally fill the visibility polygons using a rainbow colormap
#     if vis_polygons:
#         colors = {art_pieces[i]: plt.get_cmap('rainbow', len(art_pieces))(i) for i in range(len(art_pieces))}
#         for art_piece in art_pieces:
#             vis_poly = visibility_polygon(art_piece, walls)
#             x, y = vis_poly.exterior.xy
#             plt.fill(x, y, color=colors[art_piece], alpha=0.1)
#     plt.show()
