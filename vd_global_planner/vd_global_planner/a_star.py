#import 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import ipdb
import time
import math
from heapdict import heapdict
import tracemalloc
import random
from scipy import spatial as sp
import carla
import networkx as nx
from scipy.integrate import solve_ivp

class Node:
        
    def __init__(self, grid_index, cost,  parent_index):        
        self.grid_index = grid_index
        self.cost = cost         
        self.parent_index = parent_index

    def get_index(self):
        return self.grid_index


class a_star:
    
    def __init__(self, grid_map, grid_resolution, offset):
        #grid_map = 2d np array
        #map = is carla map used during collision checking 
        #lf, lr: front and rear axel distance from CG
        # W: width of a vehicle

        self.grid_map = grid_map  
        self.grid_resolution = grid_resolution      
        self.threshold = 1
        self.offset = offset 
        # self.lr = lr
        # self.lf = lf
        # self.w = w
        # self.simulation_time = 0.1 # same as controller frequency
        # self.eval_time = 0.01
        # self.angle_steps = 10    # no of loops in 1 simulation steps
        # self.accel_steps = 20
        # self.accel_min = accel_min
        # self.accel_max = acccel_max
        # self.steer_min = np.rad2deg(min_steer)
        # self.steer_max = np.rad2deg(max_steer)


    def get_path(self, open_dict,  goal_node, start_node ):
        #print("goal_node", goal_node)
        node = goal_node
        path_list = []
        while node!= start_node:
            #ispdb.set_trace()
            path_list.append(node)
            node = open_dict[node].parent_index
        path_list.append(start_node)
        path_list.reverse()
        return path_list   
    
    def cal_heuristic_cost(self, current_node, goal_node):
          
        dist = np.linalg.norm(np.array(current_node) - np.array(goal_node))           
        return dist    

    def get_neighbours(self, node):
        x_off, y_off = self.offset
        x, y = node
        # print(node)
        # print(x,y)
        rows, cols = self.grid_map.shape
        ## 8 neighbour grid

       
        n_nodes = [(x+ self.grid_resolution, y), (x-self.grid_resolution, y), (x, y+self.grid_resolution), (x, y-self.grid_resolution), 
                   (x+self.grid_resolution, y+self.grid_resolution), (x+self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y+self.grid_resolution)]
        n_list = []
        for x_val, y_val in n_nodes:
            if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                n_list.append((x_val,y_val))
      
        return n_list       



    def a_star(self, start, goal): 

        """Data strcutures
        open_set = {node_index : object}
        p_queue = {node_index : total_cost}
        closed_set = [node_index]
        """        
        goal = (int(goal[0]), int(goal[1]))
        start = (int(start[0]), int(start[1]) )

        

        p_queue = heapdict()   
        open_dict = {}
        closed_set = [] 
        rows, cols = self.grid_map.shape
        path = []

        #start node 
        start_node = Node(start, 0, None )
        open_dict[start_node.get_index()] = start_node         
        p_queue[start] = 0 + self.cal_heuristic_cost(start, goal)
        
        

        #loop until goal found or queue empty
        while p_queue:
            node,cost = p_queue.popitem() 
            node_obj = open_dict[node]
            #print("popped node", node)           
            closed_set.append(node)
            if node == goal:
                print("path found!")
                path = self.get_path(open_dict, goal, start)
                #print(path)
                return path
            else:              
                neighbour_list = self.get_neighbours(node)    
                #print("n list", neighbour_list)
                for n in neighbour_list:                
                    if n in closed_set:
                        continue  
                    
                    x,y = n

                    if n in open_dict:
                        n_node_cost = open_dict[n].cost
                    else:
                        n_node_cost = float('inf')

                    new_cost = node_obj.cost + self.grid_resolution   
                    print(int((y - self.offset[1])/self.grid_resolution))
                    print(int((x - self.offset[0])/self.grid_resolution))                 
                    if self.grid_map[ int((y - self.offset[1])/self.grid_resolution),int((x - self.offset[0])/self.grid_resolution)] == 0 and  new_cost < n_node_cost:
                        
                        if n  not in open_dict:
                            n_obj = Node(n, new_cost, node )
                            open_dict[n] = n_obj

                        open_dict[n].cost = new_cost 
                        open_dict[n].parent_index = node
                        total_cost = new_cost + self.cal_heuristic_cost(n, goal)
                        p_queue[n] = total_cost
        
        print("path not found!")             
        return path

    