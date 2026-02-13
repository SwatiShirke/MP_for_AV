import carla
import numpy as np
import matplotlib.pyplot as plt
import math

class Grid_map:
    def __init__(self, world, grd_res, buffer):
        self.world = world
        self.map = world.get_map()
        self.grid_resolution = grd_res
        self.buffer = buffer
        
    def get_grid_map(self): 

        ##get all free points at the center of all lanes
        waypoints = self.map.generate_waypoints(distance = self.grid_resolution) 

        ##from lane width find out all free points on the lanes/roads
        free_points = []
        for wp in waypoints:
            if wp.lane_type == carla.LaneType.Driving:
                lane_pts = self.expand_waypoint_to_lane_points(wp)
                #lane_pts = [(wp.transform.location.x, wp.transform.location.y )]
                free_points.extend(lane_pts)

        free_points = np.array(free_points)

        #free_points = np.array([self.snap_to_resolution((wp.transform.location.x, wp.transform.location.y)) for wp in waypoints if wp.lane_type == carla.LaneType.Driving])


        x_val = free_points[:,0]
        y_val = free_points[:,1]
        
        
        #grid creation
        x_min, x_max = min(x_val) - self.buffer, max(x_val) + self.buffer
        y_min, y_max = min(y_val) - self.buffer, max(y_val) + self.buffer
        
        self.offset = (x_min, y_min)
        x_lin = np.linspace(x_min, x_max, int((x_max - x_min)/self.grid_resolution)+1)
        y_lin = np.linspace(y_min, y_max, int((y_max - y_min)/self.grid_resolution)+1)
      
        
        X, Y = np.meshgrid(x_lin, y_lin)
        
        self.grid_map = np.ones(X.shape) 
        for x_pos, y_pos in free_points:       
            self.grid_map[int((y_pos - y_min)/self.grid_resolution), int((x_pos - x_min)/self.grid_resolution)]  = 0
            
        return self.grid_map, self.offset, self.grid_resolution  
    

    def expand_waypoint_to_lane_points(self, wp):
        loc = wp.transform.location
        yaw = math.radians(wp.transform.rotation.yaw)

        # Check for sidewalks
        left_wp = wp.get_left_lane()
        left_barrier = (self.vehicle_width/2 + 1) if left_wp and left_wp.lane_type == carla.LaneType.Sidewalk else 0.0

        right_wp = wp.get_right_lane()
        right_barrier = (self.vehicle_width/2 + 1) if right_wp and right_wp.lane_type == carla.LaneType.Sidewalk else 0.0

        # Lane half-widths on each side
        half_width_left = wp.lane_width * 0.5 - left_barrier
        half_width_right = wp.lane_width * 0.5 - right_barrier

        # Perpendicular unit vector to lane heading
        nx = math.cos(yaw + math.pi / 2.0)
        ny = math.sin(yaw + math.pi / 2.0)

        # Sample points from -half_width_left to +half_width_right
        lane_points = []

        # Compute number of samples on left and right separately
        num_samples_left = int(math.ceil(half_width_left / self.grid_resolution))
        num_samples_right = int(math.ceil(half_width_right / self.grid_resolution)) 

        # Sample left side (negative offsets)
        for i in range(num_samples_left, 0, -1):
            offset = -i * self.grid_resolution
            px = loc.x + nx * offset
            py = loc.y + ny * offset
            lane_points.append((px, py))

        # Include center point
        lane_points.append((loc.x, loc.y))

        # Sample right side (positive offsets)
        for i in range(1, num_samples_right + 1):
            offset = i * self.grid_resolution
            px = loc.x + nx * offset
            py = loc.y + ny * offset
            lane_points.append((px, py))

        return lane_points

    def plot_grid_map(self, grid_map=None):
        """
        Plot the generated grid map.
        Free space = 0 (white), Occupied = 1 (black)
        """
        if grid_map is None:
            if not hasattr(self, "grid_map"):
                raise RuntimeError("Grid map not generated yet. Call get_grid_map() first.")
            grid_map = self.grid_map

        plt.figure(figsize=(8, 8))
        plt.imshow(
            grid_map,
            origin="lower",
            cmap="gray",
            interpolation="nearest"
        )
        plt.colorbar(label="Occupancy (0=free, 1=occupied)")
        plt.title("CARLA Road Grid Map")
        plt.xlabel("X grid index")
        plt.ylabel("Y grid index")
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    def plot_grid_map_world(self, grid_map=None):
        """
        Plot grid map in CARLA world coordinates (offset-correct, cell-aligned).
        """
        import matplotlib.pyplot as plt

        if grid_map is None:
            if not hasattr(self, "grid_map"):
                raise RuntimeError("Grid map not generated yet. Call get_grid_map() first.")
            grid_map = self.grid_map

        x_min, y_min = self.offset
        h, w = grid_map.shape
        res = self.grid_resolution

        # Cell-edge aligned extents (IMPORTANT)
        x_max = x_min + w * res
        y_max = y_min + h * res

        plt.figure(figsize=(8, 8))
        plt.imshow(
            grid_map,
            origin="lower",
            cmap="gray_r",                 # 0=free (white), 1=occupied (black)
            extent=[x_min, x_max, y_min, y_max],
            interpolation="nearest"
        )

        plt.colorbar(label="Occupancy (0=free, 1=occupied)")
        plt.title("CARLA Occupancy Grid (World Coordinates)")
        plt.xlabel("World X (m)")
        plt.ylabel("World Y (m)")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    
    grid_map_generator = Grid_map(world, grd_res=1.0, buffer=10.0)
    grid_map, offset = grid_map_generator.get_grid_map()
    print(f"Grid map shape: {grid_map.shape}, Offset: {offset}")
    grid_map_generator.plot_grid_map(grid_map)
    grid_map_generator.plot_grid_map_world(grid_map)