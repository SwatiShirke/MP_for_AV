import rclpy
from rclpy.node import Node
from vd_msgs.msg import  VDpose, VDtraj



class WaypointPublisher(Node):
    def __init__(self, topic="/rl_waypoints", frame_id="map"):
        super().__init__("rl_waypoint_publisher")
        self.pub = self.create_publisher(VDtraj, topic, 10)
        self.frame_id = frame_id

    def publish_waypoints(self, waypoints, ref_velocity):
        """
        waypoints_xy: np array shape (10,2) => [[x,y],...]
        """
        waypoints = waypoints.reshape(-1, 3)  # ensure shape is (10,2)
        path_msg = VDtraj()
        


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
            pose_stamped.velocity = float(ref_velocity)
            
            path_msg.poses.append(pose_stamped) 
            #print("waypoint: ", [pose_stamped.x, pose_stamped.y, pose_stamped.psi])

        self.pub.publish(path_msg)