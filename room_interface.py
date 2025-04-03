import sys
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.validation import explain_validity
from jamico import create_poly_room, create_RecRoom
from schatten import schatten
from dictionary import createDict  
from interface import get_polygon
from scipo import find_best_combination
from guard import setGuard


def prompt_float(prompt_text, default):
    try:
        inp = input(f"{prompt_text} (default {default}): ")
        return float(inp) if inp else default
    except ValueError:
        print("Invalid input. Using default value.")
        return default

def prompt_int(prompt_text, default):
    try:
        inp = input(f"{prompt_text} (default {default}): ")
        return int(inp) if inp else default
    except ValueError:
        print("Invalid input. Using default value.")
        return default

def generate_art_pieces(user_polygon, art_piece_number):
    minx, miny, maxx, maxy = user_polygon.bounds
    art_pieces = []
    while len(art_pieces) < art_piece_number:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if user_polygon.contains(p):
            art_pieces.append(p)
    return art_pieces

def get_artworks_manual(user_polygon, walls, art_piece_number, tol=1e-6):
    """
    Interactive function to choose artwork locations manually.
    A click is accepted if:
      - It lies inside the user polygon.
      - It is not too close to any wall (distance > tol).
    Press Enter when done.
    """
    artworks = []
    fig, ax = plt.subplots()
    # Plot the room boundary
    x, y = user_polygon.exterior.xy
    ax.plot(x, y, color='blue', linewidth=1)
    # Plot existing walls in black
    for wall in walls:
        wx, wy = wall.xy
        ax.plot(wx, wy, color='black', linewidth=1)
    ax.set_title(f"Klicke {art_piece_number} Kunstwerk-Positionen.\nDrücke Enter, wenn fertig.")
    
    def on_click(event):
        if event.inaxes != ax:
            return
        candidate = Point(event.xdata, event.ydata)
        # Check candidate is inside polygon.
        if not user_polygon.contains(candidate):
            print("Klick außerhalb des Raumes. Bitte innerhalb klicken.")
            return
        # Check candidate is not too close to any wall.
        for wall in walls:
            if candidate.distance(wall) < tol:
                print("Kunstwerk liegt zu nahe an einer Wand. Bitte einen anderen Punkt wählen.")
                return
        artworks.append(candidate)
        ax.plot(candidate.x, candidate.y, 'o', color='magenta')
        fig.canvas.draw()
        print(f"Kunstwerk {len(artworks)}/{art_piece_number} platziert.")
        if len(artworks) == art_piece_number:
            plt.close(fig)

    def on_key(event):
        # Allow user to cancel the last artwork with escape.
        nonlocal artworks
        if event.key == 'escape':
            if artworks:
                removed = artworks.pop()
                print("Letzter Kunstwerk-Punkt gelöscht.")
                ax.cla()
                # redraw room boundary and walls
                x, y = user_polygon.exterior.xy
                ax.plot(x, y, color='blue', linewidth=1)
                for wall in walls:
                    wx, wy = wall.xy
                    ax.plot(wx, wy, color='black', linewidth=1)
                # redraw artwork points
                for art in artworks:
                    ax.plot(art.x, art.y, 'o', color='magenta')
                ax.set_title(f"Klicke {art_piece_number} Kunstwerk-Positionen.\nDrücke Enter, wenn fertig.")
                fig.canvas.draw()
        elif event.key == 'enter':
            if len(artworks) < art_piece_number:
                print(f"Du musst {art_piece_number} Kunstwerke platzieren.")
            else:
                plt.close(fig)

    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()
    return artworks

def get_walls_manual(user_polygon):
    """
    Interactive function to draw wall segments manually.
    Click two points for each wall segment.
    Press Esc to cancel the current segment.
    Press Enter to finish drawing walls.
    """
    walls = []
    current_points = []  # store two points for a wall
    fig, ax = plt.subplots()
    # Plot the user polygon boundary
    x, y = user_polygon.exterior.xy
    ax.plot(x, y, color='blue', linewidth=1)
    # Temporary line for current wall
    temp_line, = ax.plot([], [], marker='o', linestyle='-', color='red')
    ax.set_title("Zum Zeichnen von Wänden: jeweils 2 Klicks pro Wand.\nDrücke Enter zum Beenden, Esc zum Löschen der aktuellen Auswahl.")

    def on_click(event):
        nonlocal current_points
        if event.inaxes != ax:
            return
        current_points.append((event.xdata, event.ydata))
        if len(current_points) == 2:
            # When two points are clicked, draw the wall and store it.
            x_coords, y_coords = zip(*current_points)
            ax.plot(x_coords, y_coords, color='red', linewidth=2)
            walls.append(LineString(current_points))
            current_points = []
            fig.canvas.draw()
        else:
            # Show temporary point
            temp_line.set_data(*zip(*current_points))
            fig.canvas.draw()

    def on_key(event):
        nonlocal current_points
        if event.key == 'escape':
            current_points = []
            temp_line.set_data([], [])
            fig.canvas.draw()
            print("Aktuelle Wand-Linie gelöscht.")
        elif event.key == 'enter':
            plt.close(fig)

    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()
    return walls

def kunstwerkPolygon(kunstwerk, raumPolygon, waendeLinien):
    sichtPolygon = raumPolygon
    schattenListe = []
    for wand in waendeLinien:
        shadow = schatten(kunstwerk, wand)
        if shadow is not None:
            schattenListe.append(shadow)
    return removeShadows(sichtPolygon, schattenListe)

def removeShadows(polygon_a, shadows):
    if not polygon_a.is_valid:
        print("Invalid polygon_a:", explain_validity(polygon_a))
        return polygon_a
    for shadow in shadows:
        if shadow is None or not shadow.is_valid:
            continue
        polygon_a = polygon_a.difference(shadow)
    return polygon_a


def plot_room(raumPolygon, kunstwerkPunkte, waendeLinien):
    # Generate colors for each artwork
    colors = list(mcolors.TABLEAU_COLORS.values())
    while len(colors) < len(kunstwerkPunkte):
        colors.extend(colors)
    
    visibility_polygons = [
        kunstwerkPolygon(kunstwerk, raumPolygon, waendeLinien) for kunstwerk in kunstwerkPunkte
    ]
    
    dict_poly = createDict(visibility_polygons)
    guards = find_best_combination(list(dict_poly.keys()))

    print("guard poly: ", guards)

    # Create figure and enable fullscreen
    fig, ax = plt.subplots()
    fig.canvas.manager.full_screen_toggle()

    for i, vis_poly in enumerate(visibility_polygons):
        color = colors[i % len(colors)]
        if isinstance(vis_poly, MultiPolygon):
            for poly in vis_poly.geoms:
                x, y = poly.exterior.xy
                ax.fill(x, y, alpha=0.2, color=color)
        elif isinstance(vis_poly, Polygon):
            x, y = vis_poly.exterior.xy
            ax.fill(x, y, alpha=0.2, color=color)
        # Mark the artwork
        kunstwerk = kunstwerkPunkte[i]
        ax.plot(kunstwerk.x, kunstwerk.y, 'o', color=color)
    
    # Plot walls
    for wall in waendeLinien:
        x, y = wall.xy
        ax.plot(x, y, color='black', linewidth=1)
    
    # Plot room boundary
    x, y = raumPolygon.exterior.xy
    ax.plot(x, y, color='blue', linewidth=1)
    
    # Plot the guards
    for guardPoly in guards:
        guard = setGuard(dict_poly[list(dict_poly.keys())[guardPoly]])
        ax.plot(guard.x, guard.y, 'ko')  # Black for guards
        for kunstwerk in kunstwerkPunkte:
            line = LineString([guard, kunstwerk])
            if not any(line.intersects(wall) for wall in waendeLinien):
                x, y = line.xy
                ax.plot(x, y, color='black', alpha=0.3, linewidth=0.5)
            
    ax.set_aspect('equal', adjustable='box')
    ax.grid(False)
    plt.show()



def main():
    print("Raum-Interface")
    #devMode = input("Entwicklermodus nutzen? (j/n, default n): ")
    print("Wähle einen Raumtyp:")
    print("1) Eigenhändiges Zeichnen (Polygon) und Erzeugen des Raumes")
    print("2) Automatische Erzeugung eines rechteckigen Raumes")
    choice = input("Deine Wahl (1 oder 2, default 1): ")
    
    # if devMode.strip().lower() in ("j", "ja"):
    #     devMode = True
    # else:
    #     devMode = False

    if choice.strip() == "2":
        x_length = prompt_int("Raum-Breite (x_length)", 15)
        y_length = prompt_int("Raum-Höhe (y_length)", 15)
        # wall_density = prompt_float("Wanddichte (0.0 - 1.0)", 0.2)
        art_piece_number = prompt_int("Anzahl Kunstwerke", 5)
        room = create_RecRoom(x_length, y_length, wall_density=0.2, art_piece_number=5)
    else:
        print("Zeichne ein Polygon.")
        user_polygon = get_polygon()
        if user_polygon is None:
            sys.exit("Kein gültiges Polygon gezeichnet. Programm beendet.")
        art_piece_number = prompt_int("Anzahl Kunstwerke", 5)
        wall_mode = input("Möchtest du die Wände manuell zeichnen? (j/n, default n): ")
        walls = []
        exterior_coords = list(user_polygon.exterior.coords)
        for i in range(len(exterior_coords)):
            wall = LineString([exterior_coords[i], exterior_coords[(i + 1)%len(exterior_coords)]])
            
            walls.append(wall)

        if wall_mode.strip().lower() in ("", "n", "nein"):
            # wall_density = prompt_float("Wanddichte (0.0 - 1.0)", 0.2)
            room = create_poly_room(user_polygon, wall_density=0.2, art_piece_number=5)
            
        else:
            print("Zeichne nun die Wände (zwei Klicks pro Wand, Enter zum Beenden).")
            walls += get_walls_manual(user_polygon)
            # Option: ask if artworks should be placed manually.
            art_mode = input("Kunstwerke manuell platzieren? (j/n, default n): ")
            if art_mode.strip().lower() in ("j", "ja"):
                art_pieces = get_artworks_manual(user_polygon, walls, art_piece_number)
            else:
                art_pieces = generate_art_pieces(user_polygon, art_piece_number)
            room = (walls, art_pieces, user_polygon)
    
    # In beiden Fällen liefert room: (walls, art_pieces, raumPolygon)
    waendeLinien, kunstwerkPunkte, raumPolygon = room[0], room[1], room[2]
    

    
    plot_room(raumPolygon, kunstwerkPunkte, waendeLinien)

if __name__ == "__main__":
    main()