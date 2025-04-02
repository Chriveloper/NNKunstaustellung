import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.validation import explain_validity

points = []
fig, ax = plt.subplots()
# Line that will show the drawn polygon
line, = ax.plot([], [], marker='o', linestyle='-', color='blue')

def on_click(event):
    if event.inaxes != ax:
        return
    points.append((event.xdata, event.ydata))
    # Update the plot with the new point
    x, y = zip(*points)
    line.set_data(x, y)
    fig.canvas.draw()

def on_key(event):
    if event.key == 'enter':
        if len(points) < 3:
            print("Polygon requires at least 3 points.")
        # Close the polygon by connecting back to the first point
        polygon = Polygon(points)
        # Simplify the polygon (adjust the tolerance as needed)
        simple_polygon = polygon.simplify(0.01, preserve_topology=True)
        if not simple_polygon.is_valid:
            explanation = explain_validity(simple_polygon)
            print("Invalid polygon:", explanation)
        else:
            print("Valid polygon!")
            print("Polygon vertices:", list(simple_polygon.exterior.coords))
        # Disconnect events after finishing
        fig.canvas.mpl_disconnect(cid_click)
        fig.canvas.mpl_disconnect(cid_key)
    elif event.key == 'escape':
        # Clear points if you want to start over
        points.clear()
        line.set_data([], [])
        fig.canvas.draw()
        print("Cleared polygon points.")

cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
cid_key = fig.canvas.mpl_connect('key_press_event', on_key)

ax.set_title("Click to draw polygon vertices\nPress Enter to finish, Esc to clear")
plt.show()