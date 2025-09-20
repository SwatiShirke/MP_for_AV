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
from vd_global_planner import carla_utils 
from scipy.spatial import KDTree


class Node:       
        
    def __init__(self, grid_index,theta, velocity, steering_angle, cost,  parent_index, traj):        
        self.grid_index = grid_index
        self.theta = theta 
        self.velocity = velocity
        self.steering_angle = steering_angle 
        self.cost = cost
        self.parent_index = parent_index      
        self.traj = traj 
        
        
        
    def get_index(self):
        return self.grid_index


class a_star:
    
    def __init__(self, grid_map, grid_resolution, offset, obstacle_list, lr, lf, w, vel_min, vel_max, min_steer, max_steer, vel_steps, angle_steps, sim_time, eval_time, barrier):
        #grid_map = 2d np array
        #map = is carla map used during collision checking 
        #lf, lr: front and rear axel distance from CG
        # W: width of a vehicle

        self.grid_map = grid_map  
        self.grid_resolution = grid_resolution      
        self.threshold = 1
        self.offset = offset 
        self.obstacle_list = obstacle_list
        self.obs_tree = KDTree([p[:2] for p in obstacle_list])
        self.lr = lr
        self.lf = lf
        self.width = w
        self.simulation_time = sim_time # same as controller frequency
        self.eval_time = eval_time
        self.angle_steps = angle_steps  # no of loops in 1 simulation steps
        self.vel_steps = vel_steps
        self.vel_min = vel_min
        self.vel_max = vel_max
        self.steer_min = min_steer
        self.steer_max = max_steer
        self.open_dict = {}
        self.margin_radius = 5 
        self.barrier = barrier


    def get_path(self, goal_node, start_node ):        
        node = goal_node
        path_list = []
        while node!= start_node:
            #ispdb.set_trace()
            path_list.append(node)
            node = self.open_dict[node].parent_index
        path_list.append(start_node)
        path_list.reverse()

        

        traj = []
        
        for node in path_list:            
            traj.extend(self.open_dict[node].traj)

        return traj   
    
    def cal_heuristic_cost(self, current_node, goal_node):
          
        dist = np.linalg.norm(np.array(current_node) - np.array(goal_node))           
        return dist    

    def get_neighbours(self, node, is_hyrbid=False):
        x_off, y_off = self.offset
        x, y = node        
        rows, cols = self.grid_map.shape        
        n_list = []

        if not is_hyrbid:
            ## 8 neighbour grid
            n_nodes = [(x+ self.grid_resolution, y), (x-self.grid_resolution, y), (x, y+self.grid_resolution), (x, y-self.grid_resolution), 
                       (x+self.grid_resolution, y+self.grid_resolution), (x+self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y-self.grid_resolution), (x-self.grid_resolution, y+self.grid_resolution)]
            
            for x_val, y_val in n_nodes:
                if ( x_val >= x_off and x_val < cols-x_off and y_val >= y_off and y_val < rows - y_off ):
                    n_list.append((x_val,y_val))
        else:
            n_list = self.get_hybrid_a_star_neighbours(node)

        return n_list       

    def snap_to_resolution(self, node):
        x, y = node
        return (round(x) , round(y))

    def get_hybrid_a_star_neighbours(self, parent_node):
        """The logic for Hybrid A* simulation is built here.
        The model has 3 inputs = [accel, steer_l, steer_r]"""


        velocity_steps = [self.vel_max] if self.vel_steps == 1 else np.linspace(self.vel_min, self.vel_max, self.vel_steps)
        steer_steps = np.linspace(self.steer_min, self.steer_max, self.angle_steps)

        # print("steer_steps", steer_steps)
        # print("velocity_steps", velocity_steps)
        x_off, y_off = self.offset
        rows, cols = self.grid_map.shape 
        
        #print("steer steps ", steer_steps)
        parent_obj = self.open_dict[parent_node]
        x_current, y_current = parent_node

        theta_current, vel_current, parent_cost = parent_obj.theta, parent_obj.velocity, parent_obj.cost
        

        n_obj_list = []
        n_index_list = []
        trajectory_dict = {}
        for vel in velocity_steps:
            for steer in steer_steps:                   
                    
                    U = [vel, steer]
                    X0 = [x_current, y_current, theta_current,parent_cost ]                   
                    t_val = np.arange(0, self.simulation_time, self.eval_time)
                    sol = solve_ivp(self.ackerman_steering,(0,self.simulation_time) , X0, t_eval=t_val, 
                                args=(U,), method="RK45")
                    
                    m, n = sol.y.shape                    
                    traj = np.transpose(sol.y)                   
                    traj = np.hstack((traj, np.ones((n,1)) * vel , np.ones((n,1)) *steer))    
                    traj = traj[1:, :]              #removed to handle remove duplicate problem
                    x, y, yaw, distance, vel, steer= traj[-1, :]     # extarct the position of the node, where the simulation reached 
                    node_index = self.snap_to_resolution((x,y))

                    if node_index == parent_node or node_index in n_index_list:
                        continue


                    ##collision detection
                    center = [x_current, y_current]
                    idxs  = self.obs_tree.query_ball_point(center, r= self.margin_radius)
                    obstacle_list = [self.obstacle_list[i] for i in idxs]
                    for point in traj:
                            is_collision = self.check_collision(point, obstacle_list)   
                            if is_collision:
                                break
                                
                                
                    if is_collision:
                        continue
                    
                    if ( x >= x_off and x < cols-x_off and y >= y_off and y < rows - y_off ):                       
                                        
                        cost = abs(distance)                        
                        n_node = Node( node_index, yaw, vel, steer ,cost ,parent_node, traj)
                        n_obj_list.append(n_node)
                        trajectory_dict[node_index] = traj 
                        n_index_list.append(node_index) 

        # print("parent node ", parent_node )
        # print("n_index_list ", n_index_list)
     
        return n_obj_list
    
    def test_state_lattice_planner(self, parent_node):
        velocity_steps = np.linspace(self.vel_min, self.vel_max, self.vel_steps)
        steer_steps = np.linspace(self.steer_min, self.steer_max, self.angle_steps)
        
        x_off, y_off = self.offset
        rows, cols = self.grid_map.shape 
        
        #print("steer steps ", steer_steps)
        parent_obj = self.open_dict[parent_node]
        x_current, y_current = parent_node

        theta_current, vel_current, cost = parent_obj.theta, parent_obj.velocity, parent_obj.cost
        #print("parent_node", parent_node)
        n_obj_list = []
        n_index_list = []
        trajectory_dict = {}
        for vel in velocity_steps:
            for steer in steer_steps:                   
                    #print("vel, steer", vel, steer)
                    U = [vel, steer]
                    X = [x_current, y_current, theta_current,0 ]                   
                    t_val = np.arange(0, self.simulation_time, self.eval_time)
                    sol = solve_ivp(self.ackerman_steering,(0,self.simulation_time) , X, t_eval=t_val, 
                                args=(U,), method="RK45")
                    
                    n, _ = sol.y.shape                    
                    traj = np.transpose(sol.y)       
                    x, y, theta, distance = traj[-1]     # extarct the position of the node, where the simulation reached 
                    node_index = (x,y)
                    if node_index == parent_node or node_index in n_index_list:
                        continue
                    
                    if ( x >= x_off and x < cols-x_off and y >= y_off and y < rows - y_off ):                                                      
                        
                        trajectory_dict[node_index] = traj
                        n_index_list.append(node_index) 

        return  n_index_list   

    def check_collision(self, current_state, obstacle_list):
        """
        This function performs collision detection using Separarting axis theorem on Plytopes
        state: vehicle's current state
        obstacle_list: list of obstacles
        """

        #get vehicle's polytope corner points
        x_vd, y_vd, yaw_vd, dist, vel, steer = current_state

        R_mat = np.array([[math.cos(yaw_vd), -math.sin(yaw_vd)],
                          [math.sin(yaw_vd), math.cos(yaw_vd)]])

        half_l = (self.lf + self.lr)/2 + self.barrier
        half_w = self.width/2 + self.barrier
        corners_in_vd_frame = np.array([[x_vd + half_l, y_vd - half_w],
                                [x_vd + half_l, y_vd + half_w],
                                [x_vd - half_l, y_vd - half_w],
                                [x_vd - half_l, y_vd + half_w]])
        
        vd_corners_in_vd_world = (R_mat @ corners_in_vd_frame.T).T + np.array([x_vd, y_vd])
        x_vd_w, y_vd_w = vd_corners_in_vd_world[:,0], vd_corners_in_vd_world[:,1]
        x_min_vd, x_max_vd = np.min(x_vd_w), np.max(x_vd_w)
        y_min_vd, y_max_vd = np.min(y_vd_w), np.max(y_vd_w)

        #get obstacles corner 
        #x, y , yaw, L, W 
        for obs in obstacle_list:
            x_obs, y_obs, yaw_obs, L_obs, W_obs = obs
            half_l, half_w = L_obs /2, W_obs/2 
            R_mat_obs = np.array([[math.cos(yaw_obs), -math.sin(yaw_obs)],
                          [math.sin(yaw_obs), math.cos(yaw_obs)]])

            corners_in_obs_frame = np.array([[x_obs + half_l, y_obs - half_w],
                                [x_obs + half_l, y_obs + half_w],
                                [x_obs - half_l, y_obs - half_w],
                                [x_obs - half_l, y_obs + half_w]])

            obs_corners_in_vd_world = (R_mat_obs @ corners_in_obs_frame.T).T + np.array([x_obs, y_obs])
            x_vd_obs, y_vd_obs = obs_corners_in_vd_world[:,0], obs_corners_in_vd_world[:,1]
            x_min_obs, x_max_obs = np.min(x_vd_obs), np.max(x_vd_obs)
            y_min_obs, y_max_obs = np.min(y_vd_obs), np.max(y_vd_obs)

            ##check collision and return true if true
            ## if no collision then continue checking next obstacle
            if(x_min_vd < x_min_obs and x_max_vd < x_min_obs) or (x_min_vd > x_max_obs and x_max_vd > x_max_obs) or (y_min_vd < y_min_obs and y_max_vd < y_min_obs) or (y_min_vd > y_max_obs and y_max_vd > y_max_obs):
                continue
            else:
                return True 
            
        return False 

    def get_node_to_index(self,node):
        ##from real no (x,y) of node convert into index of an 2d array map        
        x, y = node
        x_idx = (x - self.offset[0]) /self.grid_resolution
        y_idx = (y - self.offset[1])/self.grid_resolution
        return (int(x_idx), int(y_idx)) 

    def get_index_to_node(self, index):
        x,y = index        
        node  = ((x + self.offset[0] ) * self.grid_resolution , (y + self.offset[1])* self.grid_resolution)
        return node
    

    def ackerman_steering(self, t, X, U):
        "Ackerman steering model is implemented herem it is a kinematic model"
        """
        vel: forward velocity in vehicle frame
        theta: Heading angle of vehicle in reference frame
        accel: acceleration/decceleration signal 
        steer_l, steer_r: steering angle of left and right front wheel

        """    
        x_pos, y_pos, yaw, distance = X
        vel, steer= U
        

        # Rl =  self.lf / np.tan(steer_l)  + (self.width /2)      # left inner 
        # Rr =  self.lr / np.tan(steer_r)  - (self.width /2)
        # R = (Rl + Rr)/2

        beta = np.arctan2(self.lr *  np.tan(steer), (self.lf + self.lr))

        # print("R", R)
        #print("beta", beta)
        dt = [vel * np.cos(yaw + beta),
              vel * np.sin(yaw + beta),
              vel / (self.lr) * np.sin(beta),
              vel]
        
        return dt
    

    def a_star(self, start, goal): 

        """Data strcutures
        open_set = {node_index : object}
        p_queue = {node_index : total_cost}
        closed_set = [node_index]
        """  
        x,y, yaw = start
        start = self.snap_to_resolution((x,y)) 
        goal = self.snap_to_resolution( goal)
        print("start", x," ", y," ",  yaw )
        print("goal", goal)

        p_queue = heapdict()   
        self.open_dict = {}
        closed_set = [] 
        rows, cols = self.grid_map.shape
        path = []

        #start node 
        start_node = Node(start, yaw, 0,0,0, None, [] )
        self.open_dict[start_node.get_index()] = start_node         
        p_queue[start] = 0 + self.cal_heuristic_cost(start, goal)
        
        
        explored_nodes = []
       
        #loop until goal found or queue empty
        while p_queue:
            
            node,cost = p_queue.popitem() 
            explored_nodes.append(node)         
            closed_set.append(node)
            
            
            
            if node == goal:
                print("path found!")
                path = self.get_path(goal, start)                
                return path, explored_nodes
            else:    
                         
                neighbour_list = self.get_neighbours(node, is_hyrbid=True)    
                
                for n_obj in neighbour_list:
                    
                    n_index =  n_obj.grid_index 
                    n_cost  =  n_obj.cost 
                    traj = n_obj.traj 


                    if n_index in closed_set:
                        continue  
                    
                    x,y = n_index
                    if n_index in self.open_dict:
                        n_old_cost = self.open_dict[n_index].cost
                    else:
                        self.open_dict[n_index] = n_obj
                        n_old_cost = float('inf')                                           
          
                    if self.grid_map[ int((y - self.offset[1])/self.grid_resolution),int((x - self.offset[0])/self.grid_resolution)] == 0 and  n_cost < n_old_cost:                     

                        self.open_dict[n_index].cost = n_cost 
                        self.open_dict[n_index].parent_index = node
                        self.open_dict[n_index].traj = traj
                        total_cost = n_cost + self.cal_heuristic_cost(n_index, goal)
                        p_queue[n_index] = total_cost
        
        print("path not found!")             
        return path, explored_nodes
 
def plot_grid(node, neighbour_nodes):
    # unpack points
    x_node, y_node = zip(*node)
    x_n_node, y_n_node = zip(*neighbour_nodes)

    # scatter plots
    plt.scatter(x_node, y_node, c='red', marker='o', label='Node')
    plt.scatter(x_n_node, y_n_node, c='blue', marker='x', label='Neighbour Nodes')

    # optional connecting lines
    plt.plot(x_node, y_node, 'r--', alpha=0.5)
    plt.plot(x_n_node, y_n_node, 'b--', alpha=0.5)

    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Node vs Neighbour Nodes")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    #Connect to CARLA         
   
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
          
    #map settings
    grid_resolution = 0.25    
    buffer = 10
    grid_map, offset = carla_utils.get_grid_map(world, grid_resolution, buffer)
    

    ##planner settings     
    lr = 1.28    # l = 3.86 m, w = 1.73 m 
    lf = 1.28
    width = 1.5
    vel_min = - 10
    vel_max = 10
    min_steer = np.deg2rad(-40)
    max_steer = np.deg2rad(+40) 
    vel_steps = 2
    
    angle_steps = 3
    sim_time = 0.1
    eval_time = 0.01
    L = 1  #no of nodes on horizontal for which plotting state lattice planner ()
    W = 1  #no of nodes on vertical lines for which plotting ..
    planner = a_star(grid_map, grid_resolution, offset, lr, lr, width, 
                              vel_min, vel_max, min_steer, max_steer, vel_steps, angle_steps, sim_time, eval_time)
    start = (-64, 24)
    


    start_rounded = planner.snap_to_resolution(start)
    start_index = planner.get_node_to_index(start_rounded)

    centers = []
    neighbour_nodes = []
    print(start_index)
    for x_idx in range(start_index[0], start_index[0]+L, 1):
        for y_idx in range(start_index[1], start_index[1]+ W , 1 ):           
            
            node = planner.get_index_to_node((x_idx, y_idx))            
            planner.open_dict[node] = Node(node, 0,0, 0,0, 0,  None, [])
            n_list = planner.test_state_lattice_planner(node)
            neighbour_nodes.extend(n_list)
            centers.append(node)
    
    plot_grid(centers, neighbour_nodes)



    
    



