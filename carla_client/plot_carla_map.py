import carla
import math
import numpy as np
import matplotlib.pyplot as plt


class CarlaGridMap:
    def __init__(self, world, grid_resolution, vehicle_width, buffer):
        self.world = world
        self.map = world.get_map()
        self.grid_resolution = grid_resolution
        self.vehicle_width = vehicle_width
        self.buffer = buffer
        self.grid_map = None
        self.offset = (0, 0)

    def expand_waypoint_to_lane_points(self, wp):
        loc = wp.transform.location
        yaw = math.radians(wp.transform.rotation.yaw)

        # Check for sidewalks
        left_wp = wp.get_left_lane()
        left_barrier = (self.vehicle_width / 2 + 1) if left_wp and left_wp.lane_type == carla.LaneType.Sidewalk else 0.0

        right_wp = wp.get_right_lane()
        right_barrier = (self.vehicle_width / 2 + 1) if right_wp and right_wp.lane_type == carla.LaneType.Sidewalk else 0.0

        # Lane half-widths on each side
        half_width_left = wp.lane_width * 0.5 - left_barrier
        half_width_right = wp.lane_width * 0.5 - right_barrier

        # Perpendicular unit vector to lane heading
        nx = math.cos(yaw + math.pi / 2.0)
        ny = math.sin(yaw + math.pi / 2.0)

        # Sample points from -half_width_left to +half_width_right
        lane_points = []

        num_samples_left = int(math.ceil(half_width_left / self.grid_resolution))
        num_samples_right = int(math.ceil(half_width_right / self.grid_resolution))

        # Left side
        for i in range(num_samples_left, 0, -1):
            offset = -i * self.grid_resolution
            px = loc.x + nx * offset
            py = loc.y + ny * offset
            lane_points.append((px, py))

        # Center
        lane_points.append((loc.x, loc.y))

        # Right side
        for i in range(1, num_samples_right + 1):
            offset = i * self.grid_resolution
            px = loc.x + nx * offset
            py = loc.y + ny * offset
            lane_points.append((px, py))

        return lane_points

    def get_obstacle_list(self):
        """Fetch all vehicles and walkers as obstacles."""
        actors = self.world.get_actors()
        vehicles = actors.filter("vehicle.*")
        walkers = actors.filter("walker.pedestrian.*")

        obstacle_list = []
        for v in vehicles:
            loc = v.get_location()
            obstacle_list.append((loc.x, loc.y))
        for w in walkers:
            loc = w.get_location()
            obstacle_list.append((loc.x, loc.y))

        return obstacle_list

    def get_grid_map(self):
        """Generate binary occupancy grid (0 = free, 1 = occupied)."""
        waypoints = self.map.generate_waypoints(distance=self.grid_resolution)

        free_points = []
        for wp in waypoints:
            if wp.lane_type == carla.LaneType.Driving:
                lane_pts = self.expand_waypoint_to_lane_points(wp)
                free_points.extend(lane_pts)

        free_points = np.array(free_points)
        x_val, y_val = free_points[:, 0], free_points[:, 1]

        # Define grid boundaries
        x_min, x_max = min(x_val) - self.buffer, max(x_val) + self.buffer
        y_min, y_max = min(y_val) - self.buffer, max(y_val) + self.buffer

        self.offset = (x_min, y_min)
        x_lin = np.linspace(x_min, x_max, int((x_max - x_min) / self.grid_resolution) + 1)
        y_lin = np.linspace(y_min, y_max, int((y_max - y_min) / self.grid_resolution) + 1)
        X, Y = np.meshgrid(x_lin, y_lin)

        grid_map = np.ones(X.shape)
        for x_pos, y_pos in free_points:
            iy = int(math.ceil((y_pos - y_min) / self.grid_resolution))
            ix = int(math.ceil((x_pos - x_min) / self.grid_resolution))
            if 0 <= ix < grid_map.shape[1] and 0 <= iy < grid_map.shape[0]:
                grid_map[iy, ix] = 0  # free

        obstacle_list = self.get_obstacle_list()
        self.grid_map = grid_map

        return grid_map, self.offset, obstacle_list

    def plot_patch(self, center_x, center_y, width, length):
       """Plot a local patch of the grid map centered at (center_x, center_y) with real-world axis labels."""
       if self.grid_map is None:
           print("[WARN] No grid map available. Run get_grid_map() first.")
           return

       x_min, y_min = self.offset
       cx = int((center_x - x_min) / self.grid_resolution)
       cy = int((center_y - y_min) / self.grid_resolution)
       half_w = int(width / (2 * self.grid_resolution))
       half_l = int(length / (2 * self.grid_resolution))

       x_start = max(cx - half_w, 0)
       x_end = min(cx + half_w, self.grid_map.shape[1])
       y_start = max(cy - half_l, 0)
       y_end = min(cy + half_l, self.grid_map.shape[0])

       patch = self.grid_map[y_start:y_end, x_start:x_end]

       # Compute corresponding x, y world coordinates for axis ticks
       x_coords = np.linspace(
           x_min + x_start * self.grid_resolution,
           x_min + x_end * self.grid_resolution,
           patch.shape[1]
       )
       y_coords = np.linspace(
           y_min + y_start * self.grid_resolution,
           y_min + y_end * self.grid_resolution,
           patch.shape[0]
       )

       plt.figure(figsize=(6, 6))
       plt.imshow(patch.T, origin="lower", extent=[x_coords[0], x_coords[-1], y_coords[0], y_coords[-1]], cmap="gray")
       plt.title(f"Grid patch around ({center_x:.1f}, {center_y:.1f})")
       plt.xlabel("X (meters)")
       plt.ylabel("Y (meters)")
       plt.grid(True, linestyle="--", alpha=0.4)
       plt.show()


# ==============================================================
# Example usage (run inside CARLA PythonAPI environment)
# ==============================================================

if __name__ == "__main__":
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    grid = CarlaGridMap(world, grid_resolution=0.5, vehicle_width = 1.774, buffer=5.0)
    grid_map, offset, obstacles = grid.get_grid_map()

    # Plot a patch around a given coordinate
    grid.plot_patch(center_x=-25.48, center_y=-57.7, width=100, length=100)
