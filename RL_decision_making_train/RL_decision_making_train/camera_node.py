import rclpy
from rclpy.node import Node
import carla
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.qos import QoSProfile, QoSHistoryPolicy, ReliabilityPolicy, DurabilityPolicy


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        
        # Connect to CARLA
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        
        # Get hero vehicle
        self.vehicle = None
        self.get_vehicle("hero")
        
        # Camera settings
        self.image_width = 1280
        self.image_height = 720
        self.fov = 100
        
        # Setup camera
        self.camera_sensor = None
        self.latest_image = None
        self.setup_camera()
        
        # ROS publishers
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST, 
            depth=10, 
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE
        )
        self.image_pub = self.create_publisher(Image, '/camera/rgb/image_raw', qos_profile)
        
        # CV Bridge for converting CV images to ROS messages
        self.bridge = CvBridge()
        
        # Timer for publishing images
        self.timer_period = 0.033  # ~30 Hz
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.get_logger().info("Camera node initialized successfully")

    def get_vehicle(self, role_name):
        """Find vehicle with given role_name"""
        vehicles = self.world.get_actors().filter('vehicle.*')
        for vehicle in vehicles:
            if vehicle.attributes.get('role_name') == role_name:
                self.get_logger().info(f"Found vehicle with role_name: {role_name}, ID: {vehicle.id}")
                self.vehicle = vehicle
                return
        
        if self.vehicle is None:
            raise RuntimeError(f"Vehicle with role_name '{role_name}' not found!")

    def setup_camera(self):
        """Attach RGB camera to hero vehicle"""
        blueprint_library = self.world.get_blueprint_library()
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        
        # Configure camera
        camera_bp.set_attribute('image_size_x', str(self.image_width))
        camera_bp.set_attribute('image_size_y', str(self.image_height))
        camera_bp.set_attribute('fov', str(self.fov))
        
        # Camera transform: mounted on top front of vehicle
        # x: forward, y: right, z: up
        camera_transform = carla.Transform(
            carla.Location(x=0.0, y=0.0, z=2.4),  # 2.4m above ground (roof height)
            carla.Rotation(pitch=0, yaw=0, roll=0)  # Looking forward
        )
        
        # Spawn camera and attach to vehicle
        self.camera_sensor = self.world.spawn_actor(
            camera_bp, 
            camera_transform, 
            attach_to=self.vehicle
        )
        
        # Setup callback to capture images
        self.camera_sensor.listen(self.process_image)
        
        self.get_logger().info("Camera sensor attached to hero vehicle")

        self.R_mat = np.array([[0, 0, 1],
                               [-1, 0, 0],
                               [0, 1, 0]])
        

        self.T_vec = np.array([[0],
                               [0],
                               [2.4]])
        
        self.T_mat = np.vstack((np.hstack((self.R_mat, self.T_vec)), [0, 0, 0, 1]))
   

    def process_image(self, image):
        """Callback function when camera captures an image"""
        # Convert CARLA image to numpy array
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((image.height, image.width, 4))
        
        # Convert BGRA to BGR
        bgr_image = array[:, :, :3][:, :, ::-1]
        
        # Store the latest image
        self.latest_image = bgr_image

    def timer_callback(self):
        """Publish camera images periodically"""
        if self.latest_image is not None:
            try:
                # Convert numpy array to ROS Image message
                ros_image = self.bridge.cv2_to_imgmsg(self.latest_image, encoding='bgr8')
                ros_image.header.stamp = self.get_clock().now().to_msg()
                ros_image.header.frame_id = 'camera'
                
                # Publish image
                self.image_pub.publish(ros_image)
                
            except Exception as e:
                self.get_logger().error(f"Error publishing image: {e}")

    def destroy_node(self):
        """Cleanup camera sensor"""
        if self.camera_sensor is not None:
            self.camera_sensor.destroy()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
