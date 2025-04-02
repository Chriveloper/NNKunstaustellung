from shapely.geometry import Polygon, MultiPolygon

def createDict(areas):
    dictAreas = {}
    num_polygons = len(areas)

    # Gehe durch alle möglichen Kombinationen von Polygonen
    for i in range(1, 2**num_polygons):  # i=0 (leere Menge) wird übersprungen
        intersection = None
        locKey = [False] * num_polygons  # Standardmäßig sind alle False

        for j in range(num_polygons):
            if i & (1 << j):  # Prüfe, ob das j-te Polygon in der Kombination enthalten ist
                if intersection is None:
                    intersection = areas[j]  # Starte mit dem ersten Polygon in der Kombination
                else:
                    intersection = intersection.intersection(areas[j])  # Schnittmenge berechnen

                locKey[j] = True  # Markiere dieses Polygon als Teil der Schnittmenge

        # Speichere das Ergebnis nur, wenn die Schnittmenge existiert und nicht leer ist
        if intersection and not intersection.is_empty and isinstance(intersection, (Polygon, MultiPolygon)):
            dictAreas[tuple(locKey)] = intersection

    return dictAreas
