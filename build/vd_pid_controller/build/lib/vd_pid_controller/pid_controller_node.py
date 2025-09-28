import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vd_msgs.msg import VDControlCMD, VDstate, VDtraj, VDpose
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from nav_msgs.msg import Path, Odometry
from rclpy.qos import QoSProfile, QoSHistoryPolicy, ReliabilityPolicy, DurabilityPolicy
import pandas as pd
import numpy as np 
from scipy.interpolate import interp2d
from scipy.interpolate import griddata
from vd_carla_msgs.msg import CarlaEgoVehicleControl
from scipy.interpolate import CubicSpline
import scipy.spatial as sp



    
class PIDPublisher(Node):

    def __init__(self):
        super().__init__('pid_publisher')
        self.qos_profile = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST, depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE)        
        self.state_sub = self.create_subscription(VDpose, '/carla/ego_vehicle/odometry',self.state_cb, self.qos_profile)
        self.state_sub  # prevent unused variable warning        
        #self.mpc_sub = self.create_subscription(VDControlCMD, 'mpc_cmd', self.mpc_cmd_cb, self.qos_profile)
        #self.mpc_sub  # prevent unused variable warning
        self.local_traj_sub = self.create_subscription(VDtraj, 'predicted_path', self.local_traj_cb, self.qos_profile)
        self.pub_control_cmd = self.create_publisher(CarlaEgoVehicleControl,'/carla/ego_vehicle/vehicle_control_cmd',self.qos_profile)
        self.sim_clock = self.get_clock()
        self.time_period = 0.01 #controller frequency time_callback
        self.timer = self.create_timer(self.time_period, self.timer_callback)

        self.ref_vel = 0
        self.current_vel = 0
        self.Kp = 0.7
        self.Ki = 0.01
        self.Kd = 0.2
        self.cumm_error = 0
        self.last_error = 0
        self.MAX_ACCEL = 3.0    # maximum acceleration (e.g., 3 m/s²)
        self.MAX_DECEL = -8.5  # maximum deceleration (e.g., -8 m/s², negative!)
        self.vel_delta = 1
        self.last_accel = 0.0
        self.Tf = 5.00
        self.N = 10
        #get pedal model
        path = "src/MP_for_AV/carla_client/pedal_map_data.xlsx"
        #print(path)
        self.pedal_map_fun = self.create_interpld_obj(path) 
        self.is_odom_available = False 
        self.is_traj_available = False 

    def create_interpld_obj(self, path):
        df = pd.read_csv(path)  
       
        self.points = np.column_stack((df['velocity'].values, df['acceleration'].values))       
        self.values = df['pedal'].values
    
    # The interpolation function that takes velocity and acceleration arrays
    def interpolate_pedal(self, vel_query, accel_query):
        query_points = np.column_stack((vel_query, accel_query))

        pedals_interp = griddata(self.points, self.values, query_points, method='cubic')
        if np.isnan(pedals_interp):
            pedals_interp = griddata(self.points, self.values, query_points, method='nearest')

        return pedals_interp

    def state_cb(self, msg): 
        self.is_odom_available =  True
        self.current_state =  [msg.x, msg.y, msg.psi, msg.velocity]            
        self.current_vel = msg.velocity
         
  
    def get_traj_data_struct(self, msg ):
        ##using KD_tree for fast search in trajectory
        pose_list = []
        for pose in msg.poses:
            time = pose.header.stamp.sec + pose.header.stamp.nanosec * 1e-9
            pose_i = [time, pose.x, pose.y, pose.psi, pose.velocity, pose.distance, pose.acceleration, pose.steering_angle]
            #print("pose_i", pose_i[0:5]) 
            pose_list.append(pose_i)
        #KD_tree = sp.KDTree(pose_list[:, 1:3])
        pose_list = np.array(pose_list)
        
        traj_interpld = CubicSpline(pose_list[:, 0], pose_list)
        return traj_interpld

    def local_traj_cb(self, msg): 
        self.is_traj_available = True
        ##create a KD tree for search        
        self.traj_interpld = self.get_traj_data_struct(msg)


    def timer_callback(self): 
        if self.is_odom_available and self.is_traj_available:
            # print("                  ")
            # print("here..........")
            
            now = self.get_clock().now()
            current_time = now.nanoseconds / 1e9

            #print("current time ", current_time)
            
            next_point = self.traj_interpld(current_time + self.Tf/self.N)   
            #print("next point ", next_point)         
            self.ref_vel = next_point[4]
            self.ref_accel = next_point[6]
            self.ref_steering_angle = next_point[7]


            ##apply control
            ff_cmd = self.interpolate_pedal(self.current_vel,self.ref_accel)        
            

            #apply pid here 
            error = self.ref_vel - self.current_vel
            # print("self.ref_accel",  self.ref_accel)
            # print("curr_vel",self.current_vel )
            # print("ff_cmd", ff_cmd[0])


            # print("self.ref_vel",self.ref_vel)
            # print("error", error)
            self.ref_max = self.ref_vel + self.vel_delta
            self.ref_min = self.ref_vel - self.vel_delta
            if (self.current_vel >= self.ref_min and self.current_vel <= self.ref_max):
                pid_fb_cmd = 0
                self.cumm_error += error
                self.last_error = error
            else:
                pid_fb_cmd = self.Kp * error + self.Ki * self.cumm_error + self.Kd * (error - self.last_error)
                self.cumm_error += error
                self.last_error = error  

            #print("pid_fb_cmd", pid_fb_cmd)         
            self.accel_cmd = ff_cmd[0] + pid_fb_cmd
            self.accel_cmd = min(max(self.accel_cmd, -1.0), 1.0)
            #print("self.accel_cmd", self.accel_cmd)

            msg = CarlaEgoVehicleControl()
            current_time = self.sim_clock.now() 
            msg.header.stamp = current_time.to_msg()

            #print("self.accel_cmd",self.accel_cmd )
            if self.accel_cmd >= 0:
                msg.throttle = self.accel_cmd 
                msg.steer = self.ref_steering_angle
                msg.brake = 0.0
            else:
                msg.throttle = 0.0
                msg.steer = self.ref_steering_angle
                msg.brake = -self.accel_cmd

            self.pub_control_cmd.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    pid_publisher = PIDPublisher()

    rclpy.spin(pid_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pid_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()