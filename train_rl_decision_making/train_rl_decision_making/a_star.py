
import heapq
import carla
import numpy as np
import math
from get_map import Grid_map

class Node:       
        
    def __init__(self, grid_index, parent_index, dist_from_source): 
        self.grid_index = grid_index        
        self.dist_from_source = dist_from_source               
        self.parent_index = parent_index      
                
    def get_index(self):
        return self.grid_index



class a_star:
    def __init__(self, grid_map, offset,  grid_resolution, goal_radius):
        self.grid_map = grid_map
        self.offset = offset
        self.grid_resolution = grid_resolution    
        self.goal_radius = goal_radius
        self.h , self.w = grid_map.shape
        self.N_connected_neighbour = 8
        self.turing_penalty = 50.00
        
        
    def _snap_to_resolution(self, node):
        x, y, yaw = node
        r = self.grid_resolution
        K = self.N_connected_neighbour

        # snap position
        x = round(x / r)* r
        y = round(y / r)* r

        # convert yaw (radians) -> bin index
        yaw = yaw % (2 * math.pi)
        dtheta = 2 * math.pi / K
        k = int(round(yaw / dtheta)) % K

        return (x, y, k)

    def _get_neighbours_8(self, node, is_hyrbid=False):
        x_off, y_off = self.offset
        x, y, yaw = node        
        rows, cols = self.grid_map.shape        
        n_list = []
        
        ## 8 neighbour grid
        n_nodes = [(x+ self.grid_resolution, y, 0), 
                   (x+self.grid_resolution, y+self.grid_resolution, 1),
                   (x, y+self.grid_resolution,2),
                   (x-self.grid_resolution, y+self.grid_resolution,3),
                   (x-self.grid_resolution, y, 4),
                   (x-self.grid_resolution, y-self.grid_resolution,5),
                   (x, y-self.grid_resolution, 6),
                   (x+self.grid_resolution, y-self.grid_resolution, 7)]
        
        for x_val, y_val, yaw_val in n_nodes:
            if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                n_list.append((x_val,y_val, yaw_val))
        
        n_array = np.array(n_list)
        yaw_index_delta = np.abs(n_array[:,2] - yaw)
        # print("node ",node)
        # print("neighbour yaw delta: ", yaw_index_delta)

        n_array = np.column_stack((n_array, yaw_index_delta))        
        sorted_array = n_array[np.argsort(n_array[:,3])]  
        #print("neighbour array with yaw delta: ", sorted_array)              
        n_list = [tuple(row) for row in sorted_array[:, 0:3]] 
       
        return n_list       

    def _get_neighbours(self, node):
        x, y, yaw = node  # k is bin index 0..K-1
        r = self.grid_resolution
        K = self.N_connected_neighbour
        dtheta = 2.0 * math.pi / K
    
        neighbors = []
        for k2 in range(K):
            theta = k2 * dtheta
            nx = x + r * math.cos(theta)
            ny = y + r * math.sin(theta)
    
            # snap
            nx = round(nx / r) * r
            ny = round(ny / r) * r
    
            neighbors.append((nx, ny, k2))
        if node ==  (-102, 60, 0):
            print("neighbour ", neighbors)
        return neighbors

    def _cal_heuristic_cost(self, node, goal):
        x1, y1, _ = node
        x2, y2, _ = goal
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _is_goal_within_radius(self, node, goal, radius):
        return self._cal_heuristic_cost(node, goal) <= radius

    def _get_path(self, node, start):
        path = [] 
        while node is not None:
            path.append(np.array(node))
            node = self.open_dict[node].parent_index
        path.reverse()

        return np.array(path)
        
    def find_path(self, start, goal): 
        """
        start: (x, y, yaw)
        goal: (x, y, yaw)
        path: np array [x, y, yaw] points from start to goal
        Data strcutures
        open_set = {node_index : object}
        p_queue = {node_index : total_cost}
        closed_set = [node_index]
        """  
        x_s,y_s,yaw_s = start
        start = self._snap_to_resolution((x_s,y_s, yaw_s)) 

        x_g, y_g, yaw_g = goal
        goal = self._snap_to_resolution((x_g, y_g, yaw_g)) 

        x_max , y_max = self.offset[0] + self.w * self.grid_resolution, self.offset[1] + self.h * self.grid_resolution

        if (x_s < self.offset[0] or x_s > x_max ) or (y_s < self.offset[1] or y_s > y_max) \
        or (x_g < self.offset[0] or x_g > x_max ) or (y_g < self.offset[1] or y_g > y_max):
            print("Start or goal is out of bounds!")
            return []

        self.goal = goal 
        p_queue = []
        self.open_dict = {}
        closed_set = set() 
        rows, cols = self.grid_map.shape
        path = []

        #start node 
        start_node = Node(start, None, 0)
        self.open_dict[start_node.get_index()] = start_node         
        heapq.heappush(p_queue, (0 + self._cal_heuristic_cost(start, goal), start))
        
        
        explored_nodes = []
       
        #loop until goal found or queue empty
        while p_queue:            
            node_total_cost, node = heapq.heappop(p_queue)                     
            closed_set.add(node)
            explored_nodes.append(node)
            #print("Exploring node:", node, "Total cost:", node_total_cost)
            
            
            if self._is_goal_within_radius(node, goal, 1.0):
                print("path found!")
                path = self._get_path(node, start)                
                return path
            else:    
                         
                neighbour_list = self._get_neighbours_8(node)
                #print("Neighbours of node:", neighbour_list)                
                for n_index in neighbour_list:   
                    x, y, yaw = n_index                    
                    n_cost = self.open_dict[node].dist_from_source +  self.grid_resolution + self.turing_penalty * abs(yaw - node[2]) # add cost for yaw change
                    n_old_cost = self.open_dict[n_index].dist_from_source if n_index in self.open_dict else float('inf')

                    
                    if n_index in closed_set:
                        continue                                                                                
          
                    if self.grid_map[ int((y - self.offset[1])/self.grid_resolution),int((x - self.offset[0])/self.grid_resolution)] == 0 and  n_cost < n_old_cost:                     
                        #print("exploring neighbour:" , n_index) 

                        if n_index not in self.open_dict:
                            self.open_dict[n_index] = Node(n_index, node, n_cost)
                        else: 
                            self.open_dict[n_index].dist_from_source = n_cost 
                            self.open_dict[n_index].parent_index = node                          
                        
                        total_cost = n_cost + self._cal_heuristic_cost(n_index, goal)
                        heapq.heappush(p_queue, (total_cost, n_index))
                         
        print("path not found!")             
        return None
    

if __name__ == "__main__":
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    
    grid_map_generator = Grid_map(world, 1.00, 10.0)
    grid_map, offset, resolution = grid_map_generator.get_grid_map()
    print(f"Grid map shape: {grid_map.shape}, Offset: {offset}")
    
    a_star_planner = a_star(grid_map, offset, 1.00, 2.0)
    start = (-110.96, 59.69, math.pi/2) # example start point (x, y, yaw)
    goal = (-110.96, 40.69, math.pi/2) # example goal point (x, y, yaw)
    path, explored_nodes = a_star_planner.find_path(start, goal)
    if path is None:
        print("explored nodes: ", explored_nodes)
        grid_map_generator.plot_explored_nodes(explored_nodes, start, goal)
    else:
        grid_map_generator.plot_grid_map_world(start=start, goal=goal, path=path, show_path_points=True)
    