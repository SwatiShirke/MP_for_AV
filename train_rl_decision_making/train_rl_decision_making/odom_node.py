import rclpy
from rclpy.node import Node
from vd_msgs.msg import  VDpose



class OdomPublisher(Node):
    def __init__(self, topic="/carla/ego_vehicle/odometry", frame_id="map"):
        super().__init__("vehicle_state_publisher")
        self.pub = self.create_publisher(VDpose, topic, 10)
        self.frame_id = frame_id

    def publish_waypoints(self, current_state):
        
        x,y,yaw, vx, vy, L, W = current_state
        odom_msg = VDpose()
        speed = (vx**2 + vy**2)**0.5
       
        # Position
        odom_msg.x = x
        odom_msg.y = y   
        odom_msg.psi = yaw
        odom_msg.velocity = speed        
        self.pub.publish(odom_msg) 