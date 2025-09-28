import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
import carla
import math
from vd_msgs.msg import VDPath, VDpose, VDtraj
from rclpy.qos import QoSProfile, QoSHistoryPolicy, ReliabilityPolicy, DurabilityPolicy

class StateEstimator(Node):
    def __init__(self):
        """intialize state estimator"""

        super().__init__('state_estimator')
        #self.clock = Clock() #wall clock
        # self.sim_clock = self.get_clock() #sim clock
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()

        self.vehicle = None 
        self.get_vehicle() 
        qos_profile = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST, depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE)
        self.odom_pub = self.create_publisher(VDpose, '/carla/ego_vehicle/odometry', qos_profile)
        self.time_period = 0.01 # timer period MPC frequency = 100Hz  
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
        yaw = math.radians(self.vehicle_transform.rotation.yaw)

        return (x, y, yaw, longitudinal_velocity)
 


    def publish_odometry(self): 
        x,y, yaw, vel = self.get_current_state(s_curr_flag = False)
        self.current_loc = self.vehicle.get_transform()
        odom_msg = VDpose()
       
        # Position
        odom_msg.x = x
        odom_msg.y = y   
        #yaw = yaw #(yaw  + 2 * np.pi) % (4*np.pi) - (2* np.pi)  # MPC range of Yaw - -2*pi to +2 *pi   
        odom_msg.psi = yaw
        odom_msg.velocity = vel
        #odom_msg.distance = s_current
        # Assigning longitudinal and lateral velocities to odometry message (optional fields)        
        self.odom_pub.publish(odom_msg)  


    def timer_callback(self):
            #print("inside timer")        
            """Publish odometry and trajectory data."""
            # =======================
            # Publish Odometry
            # =======================
            #publish global path to rosbag data saver, this path is not used by MPC
            
            
            self.publish_odometry()
                

def main(args=None):
    rclpy.init(args=args)
    estimator_node = StateEstimator()
    rclpy.spin(estimator_node)
    estimator_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()