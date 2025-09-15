import matplotlib.pyplot as plt
import numpy as np

# Start and updated neighbors
start = (-65, 24)
neighbors = [(-65, 20), (-59, 21), (-58, 24), (-59, 27), (-65, 28)]

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
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
plt.xticks(np.arange(np.floor(x_min), np.ceil(x_max) + 4, 4))
plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 4, 4))

plt.show()

