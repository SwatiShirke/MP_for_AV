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

class a_star:
    
    def __init__(self, grid_map, grid_resolution, offset):
        #grid_map = 2d np array
        #map = is carla map used during collision checking 
        self.grid_map = grid_map  
        self.grid_resolution = grid_resolution      
        self.threshold = 1
        self.offset = offset 

    def get_path(self, parent_dict, goal_node, start_node ):
        #print("goal_node", goal_node)
        node = goal_node
        path_list = []
        while node!= start_node:
            #ispdb.set_trace()
            path_list.append(node)
            node = parent_dict[node]
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
        n_nodes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y-1), (x-1, y+1)]
        n_list = []
        for x_val, y_val in n_nodes:
            if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                n_list.append((x_val,y_val))
        return n_list       

   
    def a_star(self, start, goal):         
        goal = (int(goal[0]), int(goal[1]))
        start = (int(start[0]), int(start[1]) )

        # print("start", start)
        # print("goal", goal)

        open_set = heapdict()    
        closed_set = [] 
        rows, cols = self.grid_map.shape
        cost_dict = {(x,y): float("inf")  for x in range(self.offset[0], cols - self.offset[0]) for y in range(self.offset[1], rows - self.offset[1])}
        parents_dict = {}
        path = []

        # add start node
        open_set[start] = 0 + self.cal_heuristic_cost(start, goal)
        cost_dict[start] = 0
        parents_dict[start] = None
        

        #loop until goal found or queue empty
        while open_set:
            node,cost = open_set.popitem() 
            #print("popped node", node)           
            closed_set.append(node)
            if node == goal:
                #print("path found!")
                path = self.get_path(parents_dict, goal, start)
                #print(path)
                return path
            else:              
                neighbour_list = self.get_neighbours(node)    
                #print("n list", neighbour_list)
                for n in neighbour_list:                
                    if n in closed_set:
                        continue  
                    
                    x,y = n
                    new_cost = cost_dict[node] + self.grid_resolution                    
                    if self.grid_map[y - self.offset[1],x - self.offset[0]] == 0 and  new_cost < cost_dict[n]:
                        
                        cost_dict[n] = new_cost 
                        parents_dict[n] = node
                        total_cost = new_cost + self.cal_heuristic_cost(n, goal)
                        open_set[n] = total_cost
        
        #print("path not found!")             
        return path
