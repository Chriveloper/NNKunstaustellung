import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.validation import explain_validity

# Function to calculate the shadow polygon for a given point and wall
def schatten(punkt, wand):
    line1 = LineString([punkt, wand.coords[0]])
    line2 = LineString([punkt, wand.coords[1]])
    extendedPoint1 = (
        wand.coords[0][0] + getScaledVector(line1)[0],
        wand.coords[0][1] + getScaledVector(line1)[1],
    )
    extendedPoint2 = (
        wand.coords[1][0] + getScaledVector(line2)[0],
        wand.coords[1][1] + getScaledVector(line2)[1],
    )
    polygon = Polygon([wand.coords[0], wand.coords[1], extendedPoint2, extendedPoint1])
    if not polygon.is_valid:
        print("Invalid shadow polygon:", explain_validity(polygon))
        return None
    return polygon

# Function to scale a vector by a fixed factor
def getScaledVector(line):
    scaleFactor = 1000  # Extend the vector by a large fixed factor
    startPoint, endPoint = line.coords[0], line.coords[1]
    vector = (endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])
    vectorLength = np.sqrt(vector[0]**2 + vector[1]**2)
    if vectorLength > 0:
        return (vector[0] * scaleFactor / vectorLength, vector[1] * scaleFactor / vectorLength)
    return (0, 0)  # Return zero vector if the length is zero
