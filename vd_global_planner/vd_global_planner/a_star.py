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
    
    def __init__(self, graph, in_map, parent_dict):
        #grap = is a dictionary with adjacency list
        #map = is carla map used during collision checking 
        self.graph = graph             
        #self.node_list = [node for node in self.graph]
        self.parent_dict = parent_dict
        self.rounded_node_list = {(int(node[0]), int(node[1])) : node for node in graph}
        #for testing
        # print(self.node_list)
        # self.kd_tree = sp.KDTree(self.node_list)
        self.nearest_K = 5
        self.resoultion = 0.5
        self.threshold = 1
        self.map = in_map

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


    def show_directed_graph(self):
        
        graph_rounded = {(round(key[0], 2), round(key[1], 2)) : [(round(val1[0], 2), round(val1[1], 2)) for val1 in val] for key, val in self.graph.items()}
        
        # Create a directed graph (DiGraph)
        G = nx.DiGraph()
        # Add edges to the DiGraph based on the dictionary
        for node, neighbors in graph_rounded.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        # Define layout (positions for nodes)
        pos = {node: node for node in graph_rounded} 

        # Create a new position dictionary with slight offset for the labels
        pos_labels = {key: (value[0] +2, value[1] + 1) for key, value in pos.items()}  # Offset labels by 0.05

        # Draw the graph with directed edges (arrows)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='darkblue')  # Use cyan for nodes
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, edge_color='black', arrowstyle='->', arrowsize=30)  # Arrow in the middle with curved edges
        nx.draw_networkx_labels(G, pos_labels, font_size=10, font_family="sans-serif")

        # Show the plot
        plt.title("Directed Graph with Arrows")
        plt.axis('off')  # Hide axes
        #plt.show()
        plt.savefig("road_graph.png", format="PNG")


    def add_goal(self, node):        
        current_node = (int(node[0]), int(node[1]))
        current_loc = carla.Location(node[0], node[1])
        start_loc = current_loc
        current_wp = self.map.get_waypoint(current_loc)
        
        while current_node not in self.rounded_node_list: 
            next_wp = current_wp.next(1.0)
            current_wp = next_wp[0]            
            current_node = (int(current_wp.transform.location.x), int(current_wp.transform.location.y))
        child_node = self.rounded_node_list[current_node]
        parent = self.parent_dict[child_node]
        dist = np.linalg.norm(np.array(parent) - np.array(node))        
        self.graph.setdefault(parent, []).append((node, dist))
        dist = np.linalg.norm(np.array(child_node) - np.array(node))        
        self.graph.setdefault(node,[]).append((child_node, dist))
        print("goal added! : ", node)

      

    def add_start(self, node): 
        #keep moving on the current path and you will find a nearest node
        current_node = (int(node[0]), int(node[1]))
        current_loc = carla.Location(node[0], node[1])
        start_loc = current_loc
        current_wp = self.map.get_waypoint(current_loc)

        #rounded_node_list = {(int(node[0]), int(node[1])) : node for node in self.node_list}
        while current_node not in self.rounded_node_list: 
            next_wp = current_wp.next(1.0)
            current_wp = next_wp[0]            
            current_node = (int(current_wp.transform.location.x), int(current_wp.transform.location.y))

        
        distance = start_loc.distance(current_wp.transform.location) 
        rounded_node = (round(node[0],2), round(node[1],2))
        self.graph.setdefault(rounded_node, []).append((self.rounded_node_list[current_node], distance))
        print("start added")
        print(self.graph[rounded_node]) 

   
    def a_star(self, start, goal):    
        self.add_start(start)
        self.add_goal(goal)  

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
            
            closed_set.append(node)
            if (int(node[0]), int(node[1])) == (int(goal[0]), int(goal[1]) ):
                print("path found!")
                path = self.get_path(parents_dict, goal, start)
                print(path)
                return path
            else:              
                #neighbour_list = [ n for n, dist in self.graph[node]]             
                neighbour_list = self.graph[node]
                #print("neighbour_list", neighbour_list)
                for n, dist in neighbour_list:                
                    if n in closed_set:
                        continue  
                    
                    
                    new_cost = cost_dict[node] + dist

                    (x,y) = n
                    if new_cost < cost_dict[n]:
                        
                        cost_dict[n] = new_cost 
                        parents_dict[n] = node
                        total_cost = new_cost + self.cal_heuristic_cost(n, goal)
                        open_set[n] = total_cost
        path = []
        print("path not found!")
        #self.show_directed_graph()
        
        return path

    