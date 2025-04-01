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
class a_star:
    #a_star
    def __init__(self, graph, in_map):
        #grap = is a dictionary with adjacency list
        #map = is carla map used during collision checking 
        self.graph = graph  
            
        self.node_list = [node for node in self.graph]
        #for testing
        # print(self.node_list)
        self.kd_tree = sp.KDTree(self.node_list)
        self.nearest_K = 5
        self.resoultion = 0.5
        self.threshold = 1
        self.map = in_map

    def get_path(self, parent_dict, goal_node, start_node ):
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
        x, y = current_node
        xg, yg = goal_node
        cost = np.sqrt((x-xg)**2 + (y-yg)**2)
        return cost    

    def get_valid_neighbour(self, node, n_list, is_goal):
        # from current node keep moving toward next node on the same lane 
        # and same direction, untill we reach any of the neighbour
        if n_list == [] or node == None : return None
        current_node = carla.Location(node[0], node[1], 0)
        current_wp = self.map.get_waypoint(current_node)
        
        print(" ")
        for neighbour in n_list:
            print(neighbour)
            neighbour_node = carla.Location(neighbour[0], neighbour[1], 0)
            neighbour_wp = self.map.get_waypoint(neighbour_node)
            if is_goal:
                if (carla.get_path(neighbour_wp, current_wp)):
                    return neighbour  
            else:
                if (carla.get_path(current_wp, neighbour_wp)):
                    return neighbour    

        return None

    def add_goal(self,goal):
        #print("goal", goal) 
        #get neighbours list
        dist, index_list = self.kd_tree.query(goal, self.nearest_K)
        n_list = [ self.node_list[index] for index in index_list]
        goal_wp = carla.Location(goal[0], goal[1])
        for node in n_list:
            #print(node)
            #find current and next waypoint 
            current_node = (node[0], node[1])
            current_loc = carla.Location(node[0], node[1])
            current_wp = self.map.get_waypoint(current_loc)
            goal_rounded = (int(goal[0]), int(goal[1]))  
            is_this_valid_node = True          
            while current_node != goal_rounded:                 
                next_wp = current_wp.next(1.0)
                next_node = (int(next_wp[0].transform.location.x), int(next_wp[0].transform.location.y))

                #direction check
                distance = np.array(next_node) - np.array(current_node)
                direction_vec1 = (distance)/ np.linalg.norm(distance, ord=1)

                distance = np.array(goal_rounded) - np.array(current_node)
                direction_vec2 = (distance)/ np.linalg.norm(distance, ord=1)

                if np.dot(direction_vec1, direction_vec2) <= 0:
                    is_this_valid_node = False
                    break

                current_wp = next_wp[0]            
                current_node = (int(current_wp.transform.location.x), int(current_wp.transform.location.y))

            if (not is_this_valid_node):
                continue
            else:
                break
        #print("current_node", current_node)
        distance =  current_wp.transform.location.distance(goal_wp)
        rounded_goal = (round(goal[0],2), round(goal[1],2))
        self.graph.setdefault(node, []).append((rounded_goal, distance))

   
    def add_start(self, node): 
        current_node = (int(node[0]), int(node[1]))
        current_loc = carla.Location(node[0], node[1])
        start_loc = current_loc
        current_wp = self.map.get_waypoint(current_loc)

        rounded_node_list = {(int(node[0]), int(node[1])) : node for node in self.node_list}
        while current_node not in rounded_node_list: 
            next_wp = current_wp.next(1.0)
            current_wp = next_wp[0]            
            current_node = (int(current_wp.transform.location.x), int(current_wp.transform.location.y))

        #print("current_node", current_node)
        distance = start_loc.distance(current_wp.transform.location) 
        rounded_node = (round(node[0],2), round(node[1],2))
        self.graph.setdefault(rounded_node, []).append((rounded_node_list[current_node], distance))

   
    def a_star(self, start, goal):    
        self.add_start(start)
        #self.add_goal(goal)        
        open_set = heapdict()    
        closed_set = [] 
        cost_dict = {node: float("inf")  for node in self.graph}
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
                return path
            else:              
                #neighbour_list = [ n for n, dist in self.graph[node]]             
                neighbour_list = self.graph[node]
                print("neighbour_list", neighbour_list)
                for n, dist in neighbour_list:                
                    if n in closed_set:
                        continue  
                    #print("neighbour", n)
                    
                    weight = dist
                    new_cost = cost_dict[node] + weight

                    (x,y) = n
                    if new_cost < cost_dict[n]:
                        
                        cost_dict[n] = new_cost 
                        parents_dict[n] = node
                        total_cost = new_cost + self.cal_heuristic_cost(n, goal)
                        open_set[n] = total_cost
        path = []
        print("path not found!")
        return path

    