from shapely.geometry import Polygon, MultiPolygon, GeometryCollection

def createDict(areas):
    print("Creating dictionary of intersections")
    dictAreas = {}
    num_polygons = len(areas)
    k = 0

    for i in range(1, 2**num_polygons):  # i=0 (empty set) is skipped
        intersection = None
        locKey = [False] * num_polygons  

        for j in range(num_polygons):
            if i & (1 << j):  
                if intersection is None:
                    intersection = areas[j]  
                else:
                    # ✅ Ensure `intersection` is valid before calling `.intersects()`
                    if not intersection.is_empty and intersection.is_valid and areas[j].is_valid:
                        try:
                            if intersection.intersects(areas[j]):
                                intersection = intersection.intersection(areas[j])
                            else:
                                intersection = None  # No intersection possible, break early
                                break  
                        except Exception as e:
                            print(f"Error during intersection at index {j}: {e}")
                            intersection = None
                            break
                    else:
                        intersection = None
                        break  

                locKey[j] = True  

        # Explicit check for the case where all are True
        if all(locKey):
            print("Checking full intersection of all polygons")

        # Handle GeometryCollection by extracting only valid Polygons / MultiPolygons
        if isinstance(intersection, GeometryCollection):
            valid_polygons = [geom for geom in intersection.geoms if isinstance(geom, (Polygon, MultiPolygon))]
            if len(valid_polygons) == 1:
                intersection = valid_polygons[0]  # Return a single Polygon/MultiPolygon
            elif len(valid_polygons) > 1:
                intersection = MultiPolygon(valid_polygons)  # Convert list to MultiPolygon
            else:
                intersection = None  # No valid geometry left

        # Check if intersection is valid and not empty
        if intersection and not intersection.is_empty and isinstance(intersection, (Polygon, MultiPolygon)):
            dictAreas[tuple(locKey)] = intersection
            print("key: ", k, locKey)
            k += 1 
        else:
            print(f"Skipping {tuple(locKey)}")

    return dictAreas
