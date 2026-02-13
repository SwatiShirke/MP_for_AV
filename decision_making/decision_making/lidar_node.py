import rclpy
from rclpy.node import Node
import carla
import numpy as np

from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header


class CarlaLidarDepthNode(Node):

    def __init__(self):
        super().__init__('carla_lidar_depth_node')

        # -----------------------------
        # Toggle for LiDAR-only testing
        # -----------------------------
        # Set True to print/publish closest obstacle distance from filtered points
        # Set False for "fusion-only" usage (publish point cloud only)
        self.enable_distance_test = False   # <-- comment/uncomment or set True/False

        # Test filter parameters (tweak as needed)
        self.test_min_x_forward = 0.0      # keep points in front (x > 0)
        self.test_lane_half_width = 5.0    # |y| < 5 meters
        self.test_ground_min_z = -2.0      # z > -2 meters (remove deep ground returns)
        self.test_ignore_closer_than = 6.0 # ignore points closer than this (meters)

        # Limit how often we log (seconds)
        self.test_log_period_s = 0.5
        self._last_log_time = self.get_clock().now()

        # -----------------------------
        # ROS publishers
        # -----------------------------
        self.dist_pub = self.create_publisher(
            Float32MultiArray,
            '/lidar/vehicle_distances',
            10
        )

        self.cloud_pub = self.create_publisher(
            PointCloud2,
            '/lidar/points',
            10
        )

        # -----------------------------
        # CARLA connection
        # -----------------------------
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()

        self.vehicle = None
        self.lidar = None

        self.get_vehicle("hero")
        self.setup_lidar()

        self.get_logger().info("LiDAR depth node initialized")

    def get_vehicle(self, role_name: str):
        vehicles = self.world.get_actors().filter('vehicle.*')
        for v in vehicles:
            if v.attributes.get('role_name') == role_name:
                self.vehicle = v
                self.get_logger().info(
                    f"Found vehicle with role_name='{role_name}', ID={v.id}"
                )
                return
        raise RuntimeError(f"Vehicle with role_name '{role_name}' not found!")

    def setup_lidar(self):
        blueprint = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')

        blueprint.set_attribute('range', '50')
        blueprint.set_attribute('rotation_frequency', '10')
        blueprint.set_attribute('channels', '32')
        blueprint.set_attribute('points_per_second', '56000')
        blueprint.set_attribute('upper_fov', '10')
        blueprint.set_attribute('lower_fov', '-30')

        lidar_transform = carla.Transform(carla.Location(x=1.20, y=0.0, z=2.8))

        self.lidar = self.world.spawn_actor(
            blueprint,
            lidar_transform,
            attach_to=self.vehicle
        )

        self.lidar.listen(self.lidar_callback)
        self.get_logger().info("LiDAR attached to ego vehicle")

    def lidar_callback(self, lidar_data):
        # CARLA format: (x, y, z, intensity)
        points = np.frombuffer(lidar_data.raw_data, dtype=np.float32).reshape(-1, 4)[:, :3]
        if points.shape[0] == 0:
            return

        # Publish PointCloud2 for RViz / fusion
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'lidar'

        cloud_msg = point_cloud2.create_cloud_xyz32(header, points.tolist())
        self.cloud_pub.publish(cloud_msg)

        # Optional: LiDAR-only test block (closest obstacle distance)
        if self.enable_distance_test:
            self._test_publish_closest_distance(points)

    # -------------------------------------------------
    # Test helper: filter points + compute closest distance
    # -------------------------------------------------
    def _test_publish_closest_distance(self, points: np.ndarray):
        # Filter: front + lane width + ground cutoff
        filt = points[
            (points[:, 0] > self.test_min_x_forward) &
            (np.abs(points[:, 1]) < self.test_lane_half_width) &
            (points[:, 2] > self.test_ground_min_z)
        ]

        if filt.shape[0] == 0:
            return

        # Euclidean distance in LiDAR frame
        distances = np.linalg.norm(filt, axis=1)

        # Ignore extremely close points (often hood/ego reflections/noise)
        distances = distances[distances > self.test_ignore_closer_than]
        if distances.size == 0:
            return

        min_distance = float(np.min(distances))

        # Throttle logs so console doesn’t spam
        now = self.get_clock().now()
        dt = (now - self._last_log_time).nanoseconds / 1e9
        if dt >= self.test_log_period_s:
            self.get_logger().info(f"[LiDAR TEST] Closest obstacle: {min_distance:.2f} m")
            self._last_log_time = now

        # Publish min distance
        msg = Float32MultiArray()
        msg.data = [min_distance]
        self.dist_pub.publish(msg)

    def destroy(self):
        try:
            if self.lidar is not None:
                self.lidar.stop()
                self.lidar.destroy()
        except Exception:
            pass


def main(args=None):
    rclpy.init(args=args)
    node = CarlaLidarDepthNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
