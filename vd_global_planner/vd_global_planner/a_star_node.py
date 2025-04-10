import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped
from vd_msgs.srv import PlannerSrv
from vd_msgs.msg import VDPath
import carla
from vd_global_planner.a_star import a_star
import numpy as np
from scipy.interpolate import CubicSpline
import scipy.spatial as sp
from rclpy.clock import Clock
import math
from std_msgs.msg import Float32
import time 
import generate_traj_function


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
         

        #for testing
        self.start = (-26.00, 130.04)
        self.goal =  (-70.49, 128.90) 
        self.path = []      # returned by a* from grid map
        self.traj_obj = Trajecotry()
        self.planner = a_star(self.grid_map, self.grid_resolution, self.offset)        
        self.is_trajectory_generated = False
        self.current_s_len = 0
        self.ref_vel = 10.00 #m/s
        self.path_kd_tree = None
        self.init_vel = 10.00 #m/s used for predicting future points
        self.min_look_ahead_distance = 0.00
        ##pub sub
        self.path_pub = self.create_publisher(VDPath, "global_path", 10)
        self.srv = self.create_service(PlannerSrv, "global_plan_srv", self.service_callback)
        self.odom_pub = self.create_publisher(Odometry, '/carla/ego_vehicle/odometry', 10)
        self.waypoints_pub = self.create_publisher(Path, '/carla/ego_vehicle/waypoints', 10)
        self.timer = self.create_timer(self.time_period, self.timer_callback)



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
        
        self.traj_obj.create_path_funs(self.path)         
        
        self.path_kd_tree = sp.KDTree(self.path)
        self.is_trajectory_generated = True
        response.message = "Global Path generated!"

        ##for testing
        s_val = np.linspace(0, self.traj_obj.track_length, 100)
        self.traj_obj.interploate(s_val)
        x_val, y_val, _, _= self.x_interpld(s_val)        
        vd_path_msg = VDPath()
        vd_path_msg.x_val = np.array(x_val).astype(float).tolist()
        vd_path_msg.y_val = np.array(y_val  ).astype(float).tolist()
        self.path_pub.publish(vd_path_msg)
        return response
       

   
      
    
    def get_current_state(self):               
        self.vehicle_transform = self.vehicle.get_transform()    
        
        # Velocity in longitudinal and lateral directions
        vehicle_velocity = self.vehicle.get_velocity()
        forward_vector = self.vehicle_transform.get_forward_vector()
        longitudinal_velocity = (vehicle_velocity.x * forward_vector.x +
                                 vehicle_velocity.y * forward_vector.y +
                                 vehicle_velocity.z * forward_vector.z)
        
        x = self.vehicle_transform.location.x
        y = self.vehicle_transform.location.y        
        yaw = self.vehicle_transform.rotation.yaw 
        return (x, y, yaw, longitudinal_velocity)

    def publish_odometry(self): 
        x,y, yaw, vel = self.get_current_state()

        odom_msg = Odometry()
        current_time = self.sim_clock.now()
        #print(current_time) 
        odom_msg.header.stamp = current_time.to_msg()
        #odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'map'

        # Position
        odom_msg.pose.pose.position.x = x
        odom_msg.pose.pose.position.y = y
        yaw = (math.radians(yaw) + 2*np.pi) % (4*np.pi) - 2*np.pi  # MPC range of Yaw - -2*pi to +2 *pi
        odom_msg.pose.pose.orientation.x = yaw

        # Assigning longitudinal and lateral velocities to odometry message (optional fields)
        odom_msg.twist.twist.linear.x = vel
        self.odom_pub.publish(odom_msg)  

    def publish_waypoints(self, N=10):       
        #Retrieve waypoints        
        waypoints = self.get_n_waypoints()

        # print("*******************printing waypoints***************************")
        # print(waypoints)
        #Create PoseArray for waypoints
        path_msg = Path()
        current_time = self.sim_clock.now()        
        path_msg.header.stamp = current_time.to_msg()
        path_msg.header.frame_id = 'map'

        way_point_list = []
        
        for i, wp in enumerate(waypoints):
            if i ==0:
                self.ref_waypoint = wp

            pose_stamped = PoseStamped()
            pose_stamped.header = path_msg.header
            current_time = self.sim_clock.now()        
            pose_stamped.header.stamp = current_time.to_msg()
            pose_stamped.pose.position.x = float(wp[0])
            pose_stamped.pose.position.y = float(wp[1])
            pose_stamped.pose.position.z = 0.0

            yaw = (math.radians(float(wp[2])) + 2*np.pi) % (4*np.pi) - 2*np.pi             
            pose_stamped.pose.orientation.x = yaw#% 2 *math.pi
            pose_stamped.pose.orientation.y = 0.0
            pose_stamped.pose.orientation.z = 0.0
            pose_stamped.pose.orientation.w = self.ref_vel  # self.vehicle.get_speed_limit()
            pose_stamped.pose
            path_msg.poses.append(pose_stamped)  
        self.waypoints_pub.publish(path_msg)


    def get_n_waypoints(self):
        x,y, yaw, vel = self.get_current_state()
        
        vel = self.ref_vel
        #print("current loc of vehicle", x,y )
        _, index = self.path_kd_tree.query([x,y], 1)
        s_init = self.s_len[index]
        
        waypoints = []             
        for i in range(1, self.N+1):  
            dist = max(i * vel * (self.Tf /self.N), self.min_look_ahead_distance)         
            s_new = s_init + dist
            x,y, yaw, kappa = self.traj_obj.traj_interpld(s_new)           
            waypoints.append((x,y,yaw))
            print("pred point ", (x,y, yaw))
            
        return waypoints    

    

    def cal_error(self):
        if self.ref_waypoint !=None and self.current_loc != None:
            norm_error =  np.sqrt((self.ref_waypoint[0] - self.current_loc.location.x)**2 + (self.ref_waypoint[1] - self.current_loc.location.y)**2)
            float_msg = Float32()
            float_msg.data = norm_error
            #print("norm_error",norm_error)
            self.err_pub.publish(float_msg)



    def timer_callback(self):
                       
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



    



