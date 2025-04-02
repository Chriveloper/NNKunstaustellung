import random
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPolygon, MultiPoint


def setGuard(poly):
    if isinstance(poly, MultiPolygon):
        poly = getMaxPoly(poly)

    all_points = generate_random_points(poly, num_points=10000)

    # Find the point with the maximum distance to all walls
    max_distance_point = max(all_points.geoms, key=lambda p: analyze_by_max_distance_to_walls(p, poly))

    print(max_distance_point)  # This point will have the maximum distance to the polygon's walls
    
    

    return max_distance_point


def getMaxPoly(multPoly):
    polygons = list(multPoly.geoms)  # list of polygons in the multipolygon
    areas = [p.area for p in polygons]  # list of areas of the polygons
    largest_index = areas.index(max(areas))  # get index of the largest area
    largest_polygon = polygons[largest_index]
    return largest_polygon


points = [(random.uniform(0, 300), random.uniform(0, 300)) for _ in range(5)]

# Create the polygon from the random points
poly = Polygon(points)


def generate_random_points(poly, num_points=100000, analysis_criteria=None):
    # Get the bounding box of the polygon
    min_x, min_y, max_x, max_y = poly.bounds
    width = max_x - min_x
    height = max_y - min_y

    # Set the maximum offset as a proportion of the polygon's dimensions (e.g., 10% of the width/height)
    max_offset_x = width
    max_offset_y = height

    # Get a representative point (guaranteed inside the polygon)
    rep_point = poly.representative_point()
    rep_x, rep_y = rep_point.x, rep_point.y

    # Generate random points around the representative point with an offset dependent on polygon size
    points = [
        Point(rep_x + random.uniform(-max_offset_x, max_offset_x),
              rep_y + random.uniform(-max_offset_y, max_offset_y))
        for _ in range(num_points)
    ]

    # Filter the points to keep only those inside the polygon
    valid_points = [p for p in points if poly.contains(p)]

    # If analysis_criteria is provided, filter based on the analysis function
    if analysis_criteria:
        valid_points = [p for p in valid_points if analysis_criteria(p)]

    # Return as a MultiPoint geometry
    return MultiPoint(valid_points)


def analyze_by_max_distance_to_walls(point, poly):
    # Get the polygon's exterior (boundary)
    exterior = poly.exterior

    # Calculate the distance to the polygon's boundary
    distance_to_walls = point.distance(exterior)

    return distance_to_walls


def plot_polygon_and_point(poly, point):
    # Plot the polygon
    x, y = poly.exterior.xy
    plt.fill(x, y, alpha=0.5, fc='blue', label="Polygon")
    plt.plot(x, y, color='blue', linewidth=2)

    # Plot the point
    plt.scatter(point.x, point.y, color='red', zorder=5, label="Max Distance Point")

    # Set axis labels
    plt.xlabel('X')
    plt.ylabel('Y')

    # Add a title and legend
    plt.title("Polygon with Point at Max Distance from Walls")
    plt.legend()

    # Display the plot
    plt.show()


# setGuard(poly)
