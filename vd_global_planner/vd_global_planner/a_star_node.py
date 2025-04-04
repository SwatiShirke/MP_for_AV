import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped
from vd_msgs.srv import PlannerSrv
import carla
from vd_global_planner.a_star import a_star
import numpy as np
from scipy.interpolate import CubicSpline
import scipy.spatial as sp
from rclpy.clock import Clock
import math
from std_msgs.msg import Float32
import time 

class GlobalPlanner(Node):
    def __init__(self):
        super().__init__('global_planner')
        #Connect to CARLA
        self.time_period = 0.05
        self.N = 10
        self.Tf = 5
        self.clock = Clock() #wall clock
        self.sim_clock = self.get_clock() #sim clock
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.resolution = 1
        self.interpld_resolution = 0.5
        self.vehicle = None
        self.get_vehicle()
        self.graph = {}
        self.parent_dict = {}
        self.get_graph()        
        self.T_pred = 0.02 
        #for testing
        self.start = (-26.00, 130.04)
        self.goal =  (-70.49, 128.90) 
        self.path = None
        self.path_way_points = []
        self.planner = a_star(self.graph, self.map, self.parent_dict)        
        self.is_trajectory_generated = False
        self.current_s_len = 0
        self.ref_vel = 10 #m/s
        self.path_kd_tree = None
        

        ##pub sub
        self.path_pub = self.create_publisher(Path, "global_path", 10)
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
           

    def get_graph(self):
        """generate map from carla"""  
              
        node_list = self.map.get_topology()
        #create undirected graph
        parent_dict = {}
        graph = {}
        for node1, node2 in node_list:
            #print(node1, node2)
            tuple1 = (round(node1.transform.location.x, 2), round(node1.transform.location.y, 2) )
            tuple2 = (round(node2.transform.location.x, 2), round(node2.transform.location.y, 2) )
            distance = node1.transform.location.distance(node2.transform.location)
            
            #print(tuple1, tuple2)
            parent_dict[tuple2] = tuple1
            graph.setdefault(tuple1, [])
            if tuple2 not in graph[tuple1]:
                graph[tuple1].append((tuple2,distance))           
        
        self.graph = graph 
        self.parent_dict = parent_dict  
        
        # print("graph**********************")
        # print(graph)
   
    def calculate_path_distance(self, start, end):
        start_loc = carla.Location( start[0],start[1])
        end_loc = carla.Location(end[0], end[1])
        current_node = start
        current_wp = self.map.get_waypoint(start_loc)
        path_dist = 0
        #current_wp = start_loc
        while (not self.check_if_reached(current_node, end)):            
            next_wp  = current_wp.next(self.resolution)
            current_node = (next_wp[0].transform.location.x, next_wp[0].transform.location.y)
            current_wp = next_wp[0]
            path_dist += self.resolution
        return path_dist


    def check_if_reached(self, node1, node2):
        if np.linalg.norm(np.array(node1)-np.array(node2) ) <= self.resolution:
            return True
        else:
            return False

    def service_callback(self, request, response):
        self.get_logger().info('started generating global path')
        self.goal = (round(request.x,2), round(request.y,2)) 
        self.path_way_points = self.planner.a_star(self.start, self.goal)
        self.calculate_path_from_wp()
        self.interploate_path()
        self.path_kd_tree = sp.cKDTree(self.path)
        self.is_trajectory_generated = True
        response.message = "Global Path generated!"
        return response

    def calculate_path_from_wp(self):
        self.path = []
        for i in range(len(self.path_way_points)-1):
            node1 = self.path_way_points[i]
            node2 = self.path_way_points[i+1]
            x_min, y_min  = node1[0], node1[1]
            x_max, y_max = node2[0], node2[1]

            #spine_path = CubicSpline([node1[0], node1[1], [node2[0],node2[1]]])            
            x_val = np.linspace(x_min, x_max, int(abs(x_max - x_min) / self.interpld_resolution))
            y_val = np.linspace(y_max, y_min, int(abs(y_max - y_min) / self.interpld_resolution))
            nodes = zip(x_val, y_val)

            for node in nodes:
                location = carla.Location(node[0], node[1])
                wp = self.map.get_waypoint(location)
                location_on_road = (wp.transform.location.x, wp.transform.location.y, wp.tranform.rotation.yaw)
                self.path.append(location_on_road) 
        # print("Here")
        # print(len(self.path))

    def interploate_path(self):        
        x_val = [x for x,y,yaw in self.path]
        y_val = [y for x,y,yaw in self.path]
        yaw_val = [yaw for x,y,yaw in self.path]
        
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

        #for testing
        # print("x, y val", x_val[4], y_val[4])
        # print("interpld", x_interpld(s_len[4]), y_interpld(s_len[4]) )


    def publish_odometry(self):        
        self.vehicle_transform = self.vehicle.get_transform()
        self.vehicle_velocity = self.vehicle.get_velocity()
        self.current_loc = self.vehicle_transform

        odom_msg = Odometry()
        current_time = self.sim_clock.now()
        #print(current_time) 
        odom_msg.header.stamp = current_time.to_msg()
        #odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'map'

        # Position
        odom_msg.pose.pose.position.x = self.vehicle_transform.location.x
        odom_msg.pose.pose.position.y = self.vehicle_transform.location.y
        odom_msg.pose.pose.position.z = self.vehicle_transform.location.z

        # Orientation: Use Yaw, Pitch, Roll (in radians)
        yaw = (math.radians(self.vehicle_transform.rotation.yaw) + 2*np.pi) % (4*np.pi) - 2*np.pi
        pitch = math.radians(self.vehicle_transform.rotation.pitch)
        roll = math.radians(self.vehicle_transform.rotation.roll)

        # Optional: Add YPR as part of the covariance field
        # This is a hack if you want to include YPR without a custom message
        odom_msg.pose.pose.orientation.x = yaw
        odom_msg.pose.pose.orientation.y = pitch
        odom_msg.pose.pose.orientation.z = roll
                
        # Velocity
        # Velocity in longitudinal and lateral directions
        forward_vector = self.vehicle_transform.get_forward_vector()
        self.longitudinal_velocity = (self.vehicle_velocity.x * forward_vector.x +
                                 self.vehicle_velocity.y * forward_vector.y +
                                 self.vehicle_velocity.z * forward_vector.z)
        
        # Assigning longitudinal and lateral velocities to odometry message (optional fields)
        odom_msg.twist.twist.linear.x = self.longitudinal_velocity
        self.odom_pub.publish(odom_msg)  


    def publish_waypoints(self, N=10):       
        #Retrieve waypoints        
        waypoints = self.get_n_waypoints()
        #Create PoseArray for waypoints
        path_msg = Path()
        current_time = self.sim_clock.now()        
        path_msg.header.stamp = current_time.to_msg()
        path_msg.header.frame_id = 'map'

        way_point_list = []
        for wp in waypoints:
            # if i ==0:
            #     self.ref_waypoint = wp.transform

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
        x,y = (self.current_loc.location.x, self.current_loc.location.y) 
        _, index = self.path_kd_tree.query((x,y), 1)
        s_init = self.s_len[index]
        waypoints = [] 
            
        for i in range(1, self.N+1):            
            s_new = s_init + i * self.longitudinal_velocity * (self.Tf /self.N)
            x = self.x_interpld(s_new)
            y = self.y_interpld(s_new)
            yaw = self.yaw_interpld(s_new)
            waypoints.append((x,y,yaw))
        return waypoints    


    # def cal_error(self):
    #     if self.ref_waypoint !=None and self.current_loc != None:
    #         norm_error =  np.sqrt((self.ref_waypoint.location.x - self.current_loc.location.x)**2 + (self.ref_waypoint.location.y - self.current_loc.location.y)**2)
    #         float_msg = Float32()
    #         float_msg.data = norm_error
    #         #print("norm_error",norm_error)
    #         self.err_pub.publish(float_msg)

    def timer_callback(self):
        a = 1 + 2
        
        if self.is_trajectory_generated:
            """Publish odometry and trajectory data."""
            # =======================
            # Publish Odometry
            # =======================
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



    



