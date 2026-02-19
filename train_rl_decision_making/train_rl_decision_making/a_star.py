
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
        
    def _snap_to_resolution(self, node):
        x, y = node
        r = self.grid_resolution
        return (round(x / r) * r, round(y / r) * r)

    def _get_neighbours(self, node, is_hyrbid=False):
        x_off, y_off = self.offset
        x, y = node        
        rows, cols = self.grid_map.shape        
        n_list = []
        
        ## 8 neighbour grid
        n_nodes = [(x+ self.grid_resolution, y), (x-self.grid_resolution, y), (x, y+self.grid_resolution), (x, y-self.grid_resolution), 
                   (x+self.grid_resolution, y+self.grid_resolution), (x+self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y+self.grid_resolution)]
        
        for x_val, y_val in n_nodes:
            if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                n_list.append((x_val,y_val))
     
        return n_list       

    def _cal_heuristic_cost(self, node, goal):
        x1, y1 = node
        x2, y2 = goal
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
        start: (x, y)
        goal: (x, y)
        path: np array [x, y] points from start to goal
        Data strcutures
        open_set = {node_index : object}
        p_queue = {node_index : total_cost}
        closed_set = [node_index]
        """  
        x,y = start
        start = self._snap_to_resolution((x,y)) 

        x_g, y_g = goal
        goal = self._snap_to_resolution((x_g, y_g)) 
                
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
            #explored_nodes.append(node)         
            closed_set.add(node)
            
            
            
            if self._is_goal_within_radius(node, goal, 1.0):
                print("path found!")
                path = self._get_path(node, start)                
                return path
            else:    
                         
                neighbour_list = self._get_neighbours(node)
                
                for n_index in neighbour_list:                    
                    n_cost = self.open_dict[node].dist_from_source +  self.grid_resolution
                    n_old_cost = self.open_dict[n_index].dist_from_source if n_index in self.open_dict else float('inf')

                    
                    if n_index in closed_set:
                        continue                                                                                 
          
                    if self.grid_map[ int((y - self.offset[1])/self.grid_resolution),int((x - self.offset[0])/self.grid_resolution)] == 0 and  n_cost < n_old_cost:                     
                        if n_index not in self.open_dict:
                            self.open_dict[n_index] = Node(n_index, node, n_cost)
                        else: 
                            self.open_dict[n_index].dist_from_source = n_cost 
                            self.open_dict[n_index].parent_index = node                          
                        
                        total_cost = n_cost + self._cal_heuristic_cost(n_index, goal)
                        heapq.heappush(p_queue, (total_cost, n_index))
                         
        print("path not found!")             
        return path
    

if __name__ == "__main__":
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    
    grid_map_generator = Grid_map(world, 1.0, 10.0)
    grid_map, offset = grid_map_generator.get_grid_map()
    print(f"Grid map shape: {grid_map.shape}, Offset: {offset}")
    
    a_star_planner = a_star(grid_map, offset, 1.0, 10.0, 1.0)
    start = (-110.96, 59.69) # example start point (x, y, yaw)
    goal = (51.00,  213.00) # example goal point (x, y, yaw)
    path = a_star_planner.a_star(start, goal)
    print("Planned path:", path) 