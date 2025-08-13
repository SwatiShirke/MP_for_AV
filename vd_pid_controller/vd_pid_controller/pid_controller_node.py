import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vd_msgs.msg import VDControlCMD, VDstate, VDtraj
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from nav_msgs.msg import Path, Odometry
from rclpy.qos import QoSProfile, QoSHistoryPolicy, ReliabilityPolicy, DurabilityPolicy
import pandas as pd
import numpy as np 
from scipy.interpolate import interp2d
from scipy.interpolate import griddata
from carla_msgs.msg import CarlaEgoVehicleControl

    
class PIDPublisher(Node):

    def __init__(self):
        super().__init__('pid_publisher')
        self.qos_profile = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST, depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE)
        self.cmd_publisher = self.create_publisher(VDControlCMD, 'pid_control_cmd', self.qos_profile)
        self.state_sub = self.create_subscription(Odometry, '/carla/ego_vehicle/odometry',self.state_cb, self.qos_profile)
        self.state_sub  # prevent unused variable warning
        # self.traj_sub = self.create_subscription(Path, '/carla/ego_vehicle/waypoints', self.traj_cb, self.qos_profile)
        # self.traj_sub  # prevent unused variable warning
        self.mpc_sub = self.create_subscription(VDControlCMD, 'mpc_cmd', self.mpc_cmd_cb, self.qos_profile)
        self.mpc_sub  # prevent unused variable warning
        self.pub_control_cmd = self.create_publisher(CarlaEgoVehicleControl,'/carla/ego_vehicle/vehicle_control_cmd',self.qos_profile)
        self.sim_clock = self.get_clock()

        self.ref_vel = 0
        self.current_vel = 0
        self.Kp = 1.0
        self.Ki = 0.01
        self.Kd = 0.2
        self.cumm_error = 0
        self.last_error = 0
        self.MAX_ACCEL = 3.0    # maximum acceleration (e.g., 3 m/s²)
        self.MAX_DECEL = -8.5  # maximum deceleration (e.g., -8 m/s², negative!)
        self.vel_delta = 1
        self.last_accel = 0.0

        #get pedal model
        path = "src/MP_for_AV/carla_client/pedal_map_data.xlsx"
        print(path)
        self.pedal_map_fun = self.create_interpld_obj(path) 
        

    def create_interpld_obj(self, path):
        df = pd.read_csv(path)    
        # Prepare points array of shape (N,2): [velocity, acceleration]
        #self.points = np.vstack((df['velocity'].values, df['acceleration'].values)).T
        self.points = np.column_stack((df['velocity'].values, df['acceleration'].values))
        print("self.points", self.points[0])
        print("shape", self.points.shape)
        # Pedal values (N,)
        self.values = df['pedal'].values
    
    # The interpolation function that takes velocity and acceleration arrays
    def interpolate_pedal(self, vel_query, accel_query):
        query_points = np.column_stack((vel_query, accel_query))

        pedals_interp = griddata(self.points, self.values, query_points, method='cubic')
        if np.isnan(pedals_interp):
            accel_interp = griddata(self.points, self.values, query_points, method='nearest')

        return pedals_interp

    def state_cb(self, msg):
        self.current_vel = msg.twist.twist.linear.x
        
        

    def mpc_cmd_cb(self, msg):
        self.ref_vel = msg.velocity
        self.ref_accel = msg.acceleration  
        self.steering_angle = msg.steering_angle

        print(" ")
        #print("self.ref_vel", self.ref_vel)
        print("self.ref_accel", self.ref_accel)
        #print("self.steering_angle", self.steering_angle)
        print("self.currentvel", self.current_vel)
        #apply feedforward here
        ff_cmd = self.interpolate_pedal(self.current_vel,self.ref_accel)
        
        print("ff_cmd", ff_cmd[0])

        #apply pid here 
        error = self.ref_vel - self.current_vel
        # print("curr_vel",self.current_vel )
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
                 
        self.accel_cmd = ff_cmd[0] + pid_fb_cmd
        self.accel_cmd = min(max(self.accel_cmd, -1.0), 1.0)
        print("self.accel_cmd", self.accel_cmd)

        msg = CarlaEgoVehicleControl()
        current_time = self.sim_clock.now() 
        msg.header.stamp = current_time.to_msg()

        print("self.accel_cmd",self.accel_cmd )
        if self.accel_cmd >= 0:
            msg.throttle = self.accel_cmd 
            msg.steer = self.steering_angle
            msg.brake = 0.0
        else:
            msg.throttle = 0.0
            msg.steer = self.steering_angle
            msg.brake = -self.accel_cmd

        self.pub_control_cmd.publish(msg)
        

        #publish data to carla 

    # def traj_cb(self, msg):        
    #     self.ref_vel = msg.poses[0].pose.orientation.w
    #     error = self.ref_vel - self.current_vel
    #     # print("curr_vel",self.current_vel )
    #     # print("self.ref_vel",self.ref_vel)
    #     # print("error", error)
    #     self.ref_max = self.ref_vel + self.vel_delta
    #     self.ref_min = self.ref_vel - self.vel_delta
    #     if (self.current_vel >= self.ref_min and self.current_vel <= self.ref_max):
    #         accel_in = self.last_accel
    #     else:
    #         accel_in = self.Kp * error + self.Ki * self.cumm_error + self.Kd * (error - self.last_error)
    #         self.cumm_error += error
    #         self.last_error = error
    #         accel_cmd = self.last_accel + accel_in #max(self.MAX_DECEL, min(accel_in, self.MAX_ACCEL))

    #     cmd_msg = VDControlCMD()
    #     cmd_msg.acceleration = accel_cmd
    #     cmd_msg.steering_angle = 0.0        
    #     self.cmd_publisher.publish(cmd_msg)
    #     self.last_accel = accel_in
        



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