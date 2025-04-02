from shapely.geometry import Polygon


def createDict(areas):
    dictAreas = {}
    num_polygons = len(areas)

    # check every combination of polygons possible
    for i in range(1, 2**num_polygons):  
        locValue = None
        locKey = [False] * num_polygons  # array locKey by default with False

        for j in range(num_polygons):
            if i & (1 << j): # Check if the j-th polygon is in the combination
                if locValue is None:
                    locValue = areas[j]  # start with the first polygon
                else:
                    locValue = locValue.intersection(areas[j])  # get the intersection of the polygons

                locKey[j] = True  # areas[j] is in the combination

        # only save the intersection if it is existing & not empty
        if locValue and not locValue.is_empty:
            dictAreas[tuple(locKey)] = locValue # saves the intersection of the polygons with the key as a tuple of booleans

    return dictAreas