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
        
    def __init__(self, grid_index, cost, traj, parent_index):        
        self.grid_index = grid_index
        self.cost = cost
        # self.steering_angle = steering_angle
        # self.direction = direction 
        self.traj = traj 
        self.parent_index = parent_index



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

       
        n_nodes = [(x+ self.grid_resolution, y), (x-self.grid_resolution, y), (x, y+self.grid_resolution), (x, y-self.grid_resolution), 
                   (x+self.grid_resolution, y+self.grid_resolution), (x+self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y+self.grid_resolution)]
        n_list = []
        for x_val, y_val in n_nodes:
            if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                n_list.append((x_val,y_val))
      
        return n_list       

    # def get_hybrid_a_star_neighbours(self, parent_node):
    #     """The logic for Hybrid A* simulation is built here.
    #     The model has 3 inputs = [accel, steer_l, steer_r]"""
    #     accel_steps = np.linspace(self.accel_min, self.accel_max, self.accel_steps)
    #     steer_l_steps = np.linspace(self.steer_min, self.steer_max, self.steer_min)
    #     steer_r_steps = np.linspace(self.steer_min, self.steer_max, self.steer_max)
    #     n_list = []

    #     for accel in accel_steps:
    #         for steer_l in steer_l_steps:
    #             for steer_r in steer_r_steps:
    #                 U = [accel, steer_l, steer_r]
    #                 X = []
    #                 sol = solve_ivp(self.ackerman_steering, self.simulation_time, X, t_eval=self.eval_time, 
    #                             args=(U), method="RK45")

    #                 traj = sol.y[:, -1]
    #                 x, y, theta = traj[-1, 0:3]     # extarct the position of the node, where the simulation reached 
    #                 cost = 0                    
    #                 parent_index = parent_node.grid_index 
    #                 n_node = Node( [x,y], cost, traj,  parent_index)
    #                 n_list.append(n_node)
        
    #     return n_list




    def ackerman_steering(self, X, U):
        "Ackerman steering model is implemented herem it is a kinematic model"
        """
        vel: forward velocity in vehicle frame
        theta: Heading angle of vehicle in reference frame
        accel: acceleration/decceleration signal 
        steer_l, steer_r: steering angle of left and right front wheel

        """    
        x_pos, y_pos, theta, vel = X
        accel, steer_l, steer_r = U
        delta = (steer_l + steer_r)/2

        Rl =  self.l / np.tan(steer_l)  + (self.W /2)      # left inner 
        Rr =  self.l / np.tan(steer_r)  - (self.W /2)
        R = (Rl + Rr)/2

        beta = np.atan2(self.lr *  np.tan(delta), (self.lf + self.lr))
        dt = [vel * np.cos(theta + beta),
              vel * np.sin(theta + beta),
              vel / R * np.cos(beta),
              accel]
        
        return dt

    

    def a_star(self, start, goal):         
        goal = (int(goal[0]), int(goal[1]))
        start = (int(start[0]), int(start[1]) )

        print("start", start)
        print("goal", goal)

        open_set = heapdict()    
        closed_set = [] 
        rows, cols = self.grid_map.shape
        cost_dict = {(round(x,1),round(y,1)): float("inf")  for x in np.arange(self.offset[0], cols - self.offset[0], self.grid_resolution) for y in np.arange(self.offset[1], rows - self.offset[1], self.grid_resolution)}
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
                print("path found!")
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
                    print(int((y - self.offset[1])/self.grid_resolution))
                    print(int((x - self.offset[0])/self.grid_resolution))                 
                    if self.grid_map[ int((y - self.offset[1])/self.grid_resolution),int((x - self.offset[0])/self.grid_resolution)] == 0 and  new_cost < cost_dict[n]:
                        
                        cost_dict[n] = new_cost 
                        parents_dict[n] = node
                        total_cost = new_cost + self.cal_heuristic_cost(n, goal)
                        open_set[n] = total_cost
        
        print("path not found!")             
        return path

    