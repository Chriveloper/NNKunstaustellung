import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.validation import explain_validity

def get_polygon():
    points = []
    user_polygon = None
    fig, ax = plt.subplots()

    fig.canvas.manager.full_screen_toggle()

    # Line to show the drawn polygon
    line, = ax.plot([], [], marker='o', linestyle='-', color='blue')

    def on_click(event):
        if event.inaxes != ax:
            return
        points.append((event.xdata, event.ydata))
        if points:
            x, y = zip(*points)
        else:
            x, y = [], []
        line.set_data(x, y)
        fig.canvas.draw()

    def on_key(event):
        nonlocal user_polygon
        if event.key == 'escape':
            points.clear()
            line.set_data([], [])
            fig.canvas.draw()
            print("Polygon cleared.")
        elif event.key == 'enter':
            if len(points) < 3:
                print("Polygon requires at least 3 points.")
                return
            candidate = Polygon(points)
            if not candidate.is_valid:
                explanation = explain_validity(candidate)
                print("Invalid polygon:", explanation)
                points.clear()
                line.set_data([], [])
                fig.canvas.draw()
                print("Please redraw the polygon.")
                return
            else:
                print("Valid polygon!")
                print("Polygon vertices:", list(candidate.exterior.coords))
                user_polygon = candidate
                plt.close(fig)

    cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
    cid_key = fig.canvas.mpl_connect('key_press_event', on_key)

    ax.set_title("Click to draw polygon vertices\nPress Enter to finish, Esc to clear")
    plt.show()
    return user_polygon