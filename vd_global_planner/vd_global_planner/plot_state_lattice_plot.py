import matplotlib.pyplot as plt
import numpy as np

# Start and updated neighbors
start = (-41.0, 4.4)
neighbors = [(-44.7, 1.8), (-42.6, -0.2), (-40.1, -0.5), (-37.8, 0.7), (-36.6, 3.3)]

# Plot start node
plt.scatter(start[1], start[0], color="red", s=100, label="Start")  # note swapped: (y,x)

# Plot neighbors
for n in neighbors:
    plt.scatter(n[1], n[0], color="blue", s=60)      # swap (y,x)
    plt.plot([start[1], n[1]], [start[0], n[0]], "k--", alpha=0.6)

# Styling: vertical axis = X, horizontal = Y
plt.gca().set_aspect("equal", adjustable="box")
plt.xlabel("Y (horizontal)")
plt.ylabel("X (vertical)")
plt.title("State Lattice - Start and Neighbors (X vertical, Y horizontal)")
plt.legend()
plt.grid(True)

# Set ticks with resolution 0.25
resolution = 3
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
plt.xticks(np.arange(np.floor(x_min), np.ceil(x_max) + resolution, resolution))
plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max) + resolution, resolution))
plt.show()

