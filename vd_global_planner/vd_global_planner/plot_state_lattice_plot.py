import matplotlib.pyplot as plt

# Start and updated neighbors
start = (-48.75, 16.5)
neighbors = [(-49.0, 16.75), (-49.25, 16.5), (-49.25, 16.75), (-48.75, 17.0), (-48.25, 16.25), (-48.75, 16.0), (-48.5, 16.25), (-48.25, 16.5)]

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
plt.show()
