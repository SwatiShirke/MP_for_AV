import carla
import numpy as np

def get_grid_map(world, grid_resolution, buffer):
        c_map = world.get_map()
        waypoints = c_map.generate_waypoints(distance = grid_resolution)        
        x_val = [wp.transform.location.x for wp in waypoints if wp.lane_type == carla.LaneType.Driving]
        y_val = [wp.transform.location.y for wp in waypoints if wp.lane_type == carla.LaneType.Driving] 
        free_points = np.column_stack([x_val,y_val])
        
        #grid creation
        x_min, x_max = int(min(x_val) - buffer), int(max(x_val) + buffer)
        y_min, y_max = int(min(y_val) - buffer), int(max(y_val) + buffer)
        
        offeset = x_min, y_min
        x_lin = np.linspace(x_min, x_max, int((x_max - x_min)/grid_resolution)+1)
        y_lin = np.linspace(y_min, y_max, int((y_max - y_min)/grid_resolution)+1)

        X, Y = np.meshgrid(x_lin, y_lin)
        
        grid_map = np.ones(X.shape) 
        for (x_pos,y_pos) in free_points:
            grid_map[int((y_pos - y_min)/grid_resolution), int((x_pos - x_min)/grid_resolution)]  = 0
        
        return grid_map, offeset