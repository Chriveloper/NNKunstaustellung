import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.validation import explain_validity

def get_polygon():
    points = []
    fig, ax = plt.subplots()
    # Line to show the drawn polygon
    line, = ax.plot([], [], marker='o', linestyle='-', color='blue')

    def on_click(event):
        if event.inaxes != ax:
            return
        points.append((event.xdata, event.ydata))
        if len(points) > 0:
            x, y = zip(*points)
        else:
            x, y = [], []
        line.set_data(x, y)
        fig.canvas.draw()

    def on_key(event):
        nonlocal user_polygon
        if event.key == 'enter':
            if len(points) < 3:
                print("Polygon requires at least 3 points.")
                return
            # Close the polygon by connecting back to the first point
            polygon = Polygon(points)
            user_polygon = polygon  # use the polygon as drawn, no simplification
            if not user_polygon.is_valid:
                explanation = explain_validity(user_polygon)
                print("Invalid polygon:", explanation)
            else:
                print("Valid polygon!")
                print("Polygon vertices:", list(user_polygon.exterior.coords))
            plt.close(fig)  # close the interface window

    user_polygon = None
    cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
    cid_key = fig.canvas.mpl_connect('key_press_event', on_key)

    ax.set_title("Click to draw polygon vertices\nPress Enter to finish, Esc to clear")
    plt.show()
    return user_polygon