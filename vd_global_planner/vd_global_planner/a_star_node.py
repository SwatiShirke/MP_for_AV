import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped
from vd_msgs.srv import PlannerSrv
from vd_msgs.msg import VDPath, VDpose, VDtraj
import carla
from vd_global_planner.a_star import a_star
import numpy as np
from scipy.interpolate import CubicSpline
import scipy.spatial as sp
from rclpy.clock import Clock
import math
from std_msgs.msg import Float32
import time 
from rclpy.qos import QoSProfile, QoSHistoryPolicy, ReliabilityPolicy, DurabilityPolicy
from vd_global_planner.traj_opt import Trajecotry

class GlobalPlanner(Node):
    def __init__(self):
        super().__init__('global_planner')
        #Connect to CARLA
        self.time_period = 0.01 # timer period f = 100Hz
        self.N = 10         #horizon 
        self.Tf = 2        # horizon time
        self.clock = Clock() #wall clock
        self.sim_clock = self.get_clock() #sim clock
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.grid_resolution = 1        
        self.buffer = 10
        self.vehicle = None
        self.get_vehicle()
        self.grid_map = None
        self.offset = (0,0)
        self.get_grid_map()       
                
         
        self.path = []      # returned by a* from grid map
        self.trajectory = []        #(x,y,theta)
        self.planner = a_star(self.grid_map, self.grid_resolution, self.offset)        
        self.is_trajectory_generated = False
        self.current_s_len = 0
        self.ref_vel = 5.00 #m/s
        self.path_kd_tree = None
        self.init_vel = 1.00 #m/s used for predicting future points
        self.goal_margin = 5.00 #m
        ##pub sub
        qos_profile = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST, depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE)
        self.path_pub = self.create_publisher(VDPath, "global_path", 1)
        self.srv = self.create_service(PlannerSrv, "global_plan_srv", self.service_callback)
        self.odom_pub = self.create_publisher(VDpose, '/carla/ego_vehicle/odometry', qos_profile)
        self.waypoints_pub = self.create_publisher(VDtraj, '/carla/ego_vehicle/waypoints', qos_profile)
        self.timer = self.create_timer(self.time_period, self.timer_callback)

        ##traj object
        self.v_min = 0
        self.v_max = 30
        self.a_min = -8.5
        self.a_max = 2.5
        self.lateral_accel = 0.1
        self.traj_obj = Trajecotry(self.v_min,self.v_max, self.a_min, self.a_min , self.lateral_accel)
        

    def get_vehicle(self):             
        self.role_name = "hero"               
        
        vehicles = self.world.get_actors().filter('vehicle.*')
        for vehicle in vehicles:
            if vehicle.attributes.get('role_name') == self.role_name:
                print(f"Found vehicle with role_name: {self.role_name}, ID: {vehicle.id}")
                self.vehicle = vehicle
        if self.vehicle == None:
            raise RuntimeError(f"Vehicle with ID {self.role_name} not found!")
           

    def get_grid_map(self):
        waypoints = self.map.generate_waypoints(distance = self.grid_resolution)        
        x_val = [wp.transform.location.x for wp in waypoints if wp.lane_type == carla.LaneType.Driving]
        y_val = [wp.transform.location.y for wp in waypoints if wp.lane_type == carla.LaneType.Driving] 
        free_points = np.column_stack([x_val,y_val])
        
        #grid creation
        x_min, x_max = int(min(x_val) - self.buffer), int(max(x_val) + self.buffer)
        y_min, y_max = int(min(y_val) - self.buffer), int(max(y_val) + self.buffer)
        
        self.offset = (x_min, y_min)
        x_lin = np.linspace(x_min, x_max, int((x_max - x_min)/self.grid_resolution)+1)
        y_lin = np.linspace(y_min, y_max, int((y_max - y_min)/self.grid_resolution)+1)

        X, Y = np.meshgrid(x_lin, y_lin)
        
        grid_map = np.ones(X.shape) 
        for (x_pos,y_pos) in free_points:
            grid_map[int((y_pos - y_min)/self.grid_resolution), int((x_pos - x_min)/self.grid_resolution)]  = 0
        self.grid_map = grid_map  
        
    def check_if_reached(self, node1, node2):
        if np.linalg.norm(np.array(node1)-np.array(node2) ) <= self.resolution:
            return True
        else:
            return False

    def service_callback(self, request, response):
        self.get_logger().info('started generating global path')
        x,y, yaw, vel = self.get_current_state()
        self.start = (x,y)
        self.goal = (request.x,request.y)
        self.path = self.planner.a_star(self.start, self.goal)
        
        if not self.path:
            response.message = "Global Path not found!"
            return response
        print("path", self.path)
        self.path_kd_tree = sp.KDTree(self.path)
        self.is_trajectory_generated = True
        response.message = "Global Path generated!"        
        self.traj_obj.create_path_funs(self.path)

        path_arr = np.array(self.path)
        vd_path_msg = VDPath()
        vd_path_msg.x_val = np.array(path_arr[:, 0]).astype(float).tolist()
        vd_path_msg.y_val = np.array(path_arr[:, 1]).astype(float).tolist()
        self.path_pub.publish(vd_path_msg)
        return response

    def cal_trajectory(self):
        trajectory = []
        for node in self.path:         
            location = carla.Location(node[0], node[1])
            wp = self.map.get_waypoint(location)
            location_on_road = (wp.transform.location.x, wp.transform.location.y, wp.transform.rotation.yaw)
            trajectory.append(location_on_road) 
        return trajectory
        

    def interploate_path(self):               
        x_val = [x for x,y,yaw in self.trajectory]
        y_val = [y for x,y,yaw in self.trajectory]
        yaw_val = [yaw for x,y,yaw in self.trajectory]
        
        #calculate track length
        s_len = [0]
        s_point =0
        for i in range(len(x_val)-1):      
            point1 = np.array([x_val[i], y_val[i]])
            point2 = np.array([x_val[i+1], y_val[i+1]])
            dist = np.linalg.norm(point2-point1)           
            s_point += dist
            s_len.append(s_point)

        self.x_interpld = CubicSpline(s_len, x_val)
        self.y_interpld = CubicSpline(s_len, y_val)
        self.yaw_interpld = CubicSpline(s_len, yaw_val)
        self.s_len = s_len

        ##for testing
        s_val = np.linspace(0, s_len[-1], 100)
        x_val = self.x_interpld(s_val)
        y_val = self.y_interpld(s_val)

        vd_path_msg = VDPath()
        vd_path_msg.x_val = np.array(x_val).astype(float).tolist()
        vd_path_msg.y_val = np.array(y_val  ).astype(float).tolist()
        self.path_pub.publish(vd_path_msg)

    def get_current_state(self, s_curr_flag = False):               
        self.vehicle_transform = self.vehicle.get_transform()    
        
        # Velocity in longitudinal and lateral directions
        vehicle_velocity = self.vehicle.get_velocity()
        #print("vehicle_velocity", vehicle_velocity)
        forward_vector = self.vehicle_transform.get_forward_vector()
        longitudinal_velocity = (vehicle_velocity.x * forward_vector.x +
                                 vehicle_velocity.y * forward_vector.y )
        
        x = self.vehicle_transform.location.x
        y = self.vehicle_transform.location.y        
        yaw = np.deg2rad(self.vehicle_transform.rotation.yaw)

        if s_curr_flag == True:
            _, index = self.path_kd_tree.query([x,y], 1)
            s_current = self.traj_obj.waypoints[index][4] 
            return (x, y, yaw, longitudinal_velocity, s_current)
        else:
            return (x, y, yaw, longitudinal_velocity)
        

    def publish_odometry(self): 
        x,y, yaw, vel, s_current = self.get_current_state(s_curr_flag = True)
        odom_msg = VDpose()
        # current_time = self.sim_clock.now()
        # #print(current_time) 
        # odom_msg.header.stamp = current_time.to_msg()
        # #odom_msg.header.stamp = self.get_clock().now().to_msg()
        # odom_msg.header.frame_id = 'map'

        # Position
        odom_msg.x = x
        odom_msg.y = y        
        odom_msg.psi = yaw
        odom_msg.velocity = vel
        odom_msg.distance = s_current
        # Assigning longitudinal and lateral velocities to odometry message (optional fields)        
        self.odom_pub.publish(odom_msg)  

    def publish_waypoints(self, N=10):       
        #Retrieve waypoints        
        waypoints, s_total = self.get_n_waypoints()
        
        # print("*******************printing waypoints***************************")
        # print(waypoints)
        #Create PoseArray for waypoints
        path_msg = VDtraj()
        # current_time = self.sim_clock.now()        
        # path_msg.header.stamp = current_time.to_msg()
        # path_msg.header.frame_id = 'map'

        way_point_list = []        
        for i, wp in enumerate(waypoints):
            if i ==0:
                self.ref_waypoint = wp

            pose_stamped = VDpose()
            # pose_stamped.header = path_msg.header
            # current_time = self.sim_clock.now()        
            # pose_stamped.header.stamp = current_time.to_msg()
            pose_stamped.x = float(wp[0])  #x pose
            pose_stamped.y = float(wp[1])  #y pose
            pose_stamped.psi = float(wp[2])  # s_total 
            #yaw =  #(math.radians(float(wp[2])) + 2*np.pi) % (4*np.pi) - 2*np.pi              
            pose_stamped.velocity = float(wp[3])
            pose_stamped.total_distance = s_total  ##total track length     
            path_msg.poses.append(pose_stamped) 

        self.waypoints_pub.publish(path_msg)


    def is_goal_reached(self, point):
        dist = np.sqrt((self.goal[0] - point[0])**2 + (self.goal[1] - point[1])**2)
        #print("dist", dist)
        if dist <= self.goal_margin:
            return True
        else:
            return False


    def get_n_waypoints(self):
        x,y, yaw, vel, s_current = self.get_current_state(s_curr_flag = True)
        print("current state yaw", yaw)        
        goal_flag = self.is_goal_reached((x,y))              
        vel = self.ref_vel
        waypoints = []
        
        s_total = self.traj_obj.track_length
        s_init = s_current
        
        if goal_flag:
            point = self.traj_obj.traj_interpld(s_init)
            yaw = point[2]
            waypoints = [(self.goal[0], self.goal[1], yaw, 0)]
            
        else:                        
                     
            for i in range(1, self.N+1):  
                dist = max(i * vel * (self.Tf /self.N), 1)         
                s_new = s_init + dist
                point = self.traj_obj.traj_interpld(s_new)
                x = point[0]#self.x_interpld(s_new)
                y = point[1]#self.y_interpld(s_new)
                yaw = point[2]#self.yaw_interpld(s_new)
                #location = carla.Location(x=float(x), y=float(y), z=0.0)
                # waypoint = self.map.get_waypoint(location)
                # x = waypoint.transform.location.x
                # y = waypoint.transform.location.y
                # yaw = waypoint.transform.rotation.yaw
                waypoints.append((x,y,yaw, self.ref_vel))            
            
        return waypoints, s_total   


    # def get_time_spanned_waypoints(self):
    #     """
    #     Generate waypoints spaced at consistent time intervals.
    
    #     Args:
    #         vehicle: CARLA vehicle object
    #         map: CARLA map object
    #         total_time: Total time horizon (seconds)
    #         delta_t: Time interval between waypoints (seconds)
    
    #     Returns:
    #         List of time-spanned waypoints
    #     """
    #     map = self.vehicle.get_world().get_map()
    #     current_waypoint = map.get_waypoint(self.vehicle.get_transform().location)
    #     waypoints = []
    #     #print("starting here")
    #     for _ in range(int(self.N)):
    #         velocity = self.vehicle.get_velocity()
    #         forward_vector = self.vehicle.get_transform().get_forward_vector()
    #         longitudinal_speed = (velocity.x * forward_vector.x +
    #                               velocity.y * forward_vector.y +
    #                               velocity.z * forward_vector.z)
    #         # Calculate the distance to the next waypoint
    #         distance = max(longitudinal_speed * self.Tf / self.N, 1 ) # Ensure non-zero distance
    #         #print("dist ", distance)
    #         next_waypoints = current_waypoint.next(distance)
    #         #print("next wp :",next_waypoints[0].transform.location.x, next_waypoints[0].transform.location.y  )
        
    #         if next_waypoints:
    #             current_waypoint = next_waypoints[0]  # Use the first waypoint in the list
    #             waypoints.append(current_waypoint)
    #         else:
    #             break  # No more waypoints available (end of the road)
            
    #     return waypoints

    # def publish_waypoints(self, N=10):               
    #     # Retrieve waypoints
    #     waypoints = self.get_time_spanned_waypoints()
    #     #Create PoseArray for waypoints
    #     path_msg = VDtraj()
    #     current_time = self.sim_clock.now()        
    #     # path_msg.header.stamp = current_time.to_msg()
    #     # path_msg.header.frame_id = 'map'

    #     way_point_list = []
    #     for i, wp in enumerate(waypoints):
    #         if i ==0:
    #             self.ref_waypoint = wp.transform

    #         pose_stamped = VDpose()
    #         # pose_stamped.header = path_msg.header
    #         current_time = self.sim_clock.now()        
    #         # pose_stamped.header.stamp = current_time.to_msg()
    #         pose_stamped.x = wp.transform.location.x
    #         pose_stamped.y = wp.transform.location.y
    #         pose_stamped.psi = (math.radians(wp.transform.rotation.yaw) + 2*np.pi) % (4*np.pi) - 2*np.pi
    #         pose_stamped.velocity = self.ref_vel   
    #         pose_stamped.total_distance = 0.0        
    #         path_msg.poses.append(pose_stamped)  
    #     self.waypoints_pub.publish(path_msg)


    def cal_error(self):
        if self.ref_waypoint !=None and self.current_loc != None:
            norm_error =  np.sqrt((self.ref_waypoint[0] - self.current_loc.location.x)**2 + (self.ref_waypoint[1] - self.current_loc.location.y)**2)
            float_msg = Float32()
            float_msg.data = norm_error
            #print("norm_error",norm_error)
            self.err_pub.publish(float_msg)

    def timer_callback(self):
        #print("inside timer")              
        if self.is_trajectory_generated:
            """Publish odometry and trajectory data."""
            # =======================
            # Publish Odometry
            # =======================
            #publish global path to rosbag data saver, this path is not used by MPC
            
            
            self.publish_odometry()
            #cal nd publish norm error 
            #self.cal_error()
            # =======================
            # Publish Trajectory
            # =======================
            self.publish_waypoints()



def main(args=None):
    rclpy.init(args=args)
    planner_node = GlobalPlanner()
    rclpy.spin(planner_node)

    planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



    



