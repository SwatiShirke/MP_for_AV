import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from carla_msgs.msg import CarlaEgoVehicleControl
from std_msgs.msg import Header
import numpy as np 
class CarlaControllerNode(Node):
    def __init__(self):
        super().__init__('carla_controller_node')

        # Subscriber to the /carla/ego_vehicle/waypoints topic
        self.waypt_sub = self.create_subscription(
            Path,  # Message type for trajectory
            '/carla/ego_vehicle/waypoints',  # Topic for vehicle trajectory (waypoints)
            self.waypoints_callback,
            10
        )

        # Subscriber to the /carla/ego_vehicle/odometry topic
        self.odom_sub = self.create_subscription(
            Odometry,  # Message type for vehicle state
            '/carla/ego_vehicle/odometry',  # Topic for vehicle odometry (state)
            self.odometry_callback,
            10
        )

        # Publisher for control commands
        self.control_pub = self.create_publisher(
            CarlaEgoVehicleControl,
            '/carla/ego_vehicle/vehicle_control_cmd',
            10
        )

        # Variables to store state and trajectory
        self.current_trajectory = None
        self.current_odometry = None

        self.timer = self.create_timer(0.1, self.control_callback)  # Control loop at 10Hz

    def waypoints_callback(self, msg):
        """Callback for vehicle trajectory (waypoints)."""
        self.current_trajectory = msg
        self.get_logger().info(f"Received trajectory with {len(msg.poses)} waypoints.")

    def odometry_callback(self, msg):
        """Callback for vehicle odometry (state)."""
        self.current_odometry = msg
        self.get_logger().info(f"Received odometry: position ({msg.pose.pose.position.x}, {msg.pose.pose.position.y})")

    def control_callback(self):
        """Compute and publish control commands."""
        #if self.current_trajectory is None or self.current_odometry is None:
        #    return

        # Example control logic (you can replace this with your MPC or other logic)
        control_msg = CarlaEgoVehicleControl()
        control_msg.header = Header()
        control_msg.header.stamp = self.get_clock().now().to_msg()

        # Example control values
        control_msg.throttle = 0.01  # Constant throttle
        control_msg.steer =  np.deg2rad(7)/ np.deg2rad(35)   # No steering (you can compute this from trajectory)
        control_msg.brake = 0.0  # No brake
        control_msg.hand_brake = False
        control_msg.reverse = False
        control_msg.gear = 1  # First gear
        control_msg.manual_gear_shift = False

        self.control_pub.publish(control_msg)
        #self.get_logger().info(f"Published control: {control_msg}")

def main(args=None):
    rclpy.init(args=args)
    node = CarlaControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
