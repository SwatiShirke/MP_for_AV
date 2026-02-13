import rclpy
from rclpy.node import Node
import numpy as np

from sensor_msgs.msg import PointCloud2, CameraInfo
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Float32MultiArray

from vision_msgs.msg import Detection2DArray

from message_filters import Subscriber, ApproximateTimeSynchronizer


class CarlaFusionNode(Node):
    """
    Fuses YOLO 2D detections + LiDAR PointCloud2 to estimate 3D positions.

    Inputs:
      - /camera/camera_info           (CameraInfo)  frame_id="camera"
      - /perception/detections2d      (Detection2DArray)
      - /lidar/points                 (PointCloud2)

    Output:
      - /perception/fused_obstacles   (Float32MultiArray)
        Flattened list per detection:
        [cls_id, score, X_ego, Y_ego, Z_ego, range_m] repeated...
    """

    def __init__(self):
        super().__init__("carla_fusion_node")

        # ----------------------------
        # Subscribers
        # ----------------------------
        self.caminfo_sub = self.create_subscription(
            CameraInfo, "/camera/camera_info", self.on_caminfo, 10
        )

        self.det_sub = Subscriber(self, Detection2DArray, "/perception/detections2d")
        self.lidar_sub = Subscriber(self, PointCloud2, "/lidar/points")

        # Approx time sync (tune slop if needed)
        self.ts = ApproximateTimeSynchronizer(
            [self.det_sub, self.lidar_sub],
            queue_size=10,
            slop=0.10  # seconds
        )
        self.ts.registerCallback(self.synced_callback)

        # ----------------------------
        # Publisher
        # ----------------------------
        self.fused_pub = self.create_publisher(
            Float32MultiArray,
            "/perception/fused_obstacles",
            10
        )

        # ----------------------------
        # Camera intrinsics cache
        # ----------------------------
        self.K = None
        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None
        self.img_w = None
        self.img_h = None

        # ----------------------------
        # Extrinsics (vehicle frame assumptions)
        # ----------------------------
        # From your nodes:
        #   LiDAR mounted at z=2.8
        #   Camera mounted at z=2.4
        # Both at x=y=0, roll=pitch=yaw=0
        #
        # We assume LiDAR and camera are aligned with vehicle axes (CARLA sensor frame):
        #   x forward, y right, z up
        #
        # Then we convert into camera optical coords for projection:
        #   X_cam = y_vehicle (right)
        #   Y_cam = -z_vehicle (down)
        #   Z_cam = x_vehicle (forward)
        #
        self.lidar_pos_ego = np.array([1.2, 0.0, 2.8], dtype=np.float32)
        self.cam_pos_ego = np.array([0.0, 0.0, 2.4], dtype=np.float32)

        # Association / robustness parameters
        self.min_points_in_bbox = 10
        self.bbox_pixel_margin = 10.0           # enlarge bbox slightly for sparse returns
        self.depth_percentile_low = 20.0
        self.depth_percentile_high = 80.0

        self.get_logger().info("Fusion node initialized.")

    def on_caminfo(self, msg: CameraInfo):
        # Cache intrinsics
        self.img_w = msg.width
        self.img_h = msg.height

        # K is row-major 3x3 in msg.k
        self.fx = float(msg.k[0])
        self.fy = float(msg.k[4])
        self.cx = float(msg.k[2])
        self.cy = float(msg.k[5])

        self.K = np.array(msg.k, dtype=np.float32).reshape(3, 3)

    # ----------------------------
    # Core callback
    # ----------------------------
    def synced_callback(self, det_msg: Detection2DArray, cloud_msg: PointCloud2):
        if self.K is None:
            self.get_logger().warn("No CameraInfo yet. Waiting...")
            return

        # Convert PointCloud2 -> Nx3 (LiDAR frame)
        pts_lidar = self.pointcloud2_to_xyz(cloud_msg)
        if pts_lidar is None or pts_lidar.shape[0] == 0:
            return

        # Convert LiDAR points into ego/vehicle frame (translation only, since LiDAR rot=0)
        pts_ego = pts_lidar + self.lidar_pos_ego[None, :]

        # Convert ego -> camera origin (vehicle translation only)
        pts_rel_cam_origin_ego = pts_ego - self.cam_pos_ego[None, :]

        # Map CARLA vehicle coords (x fwd, y right, z up) to camera optical coords:
        # X_cam = y
        # Y_cam = -z
        # Z_cam = x
        Xc = pts_rel_cam_origin_ego[:, 1]
        Yc = -pts_rel_cam_origin_ego[:, 2]
        Zc = pts_rel_cam_origin_ego[:, 0]

        # Keep points in front of camera
        in_front = Zc > 0.1
        Xc, Yc, Zc = Xc[in_front], Yc[in_front], Zc[in_front]
        pts_ego_front = pts_ego[in_front]  # keep ego coords for output

        if Zc.size == 0:
            return

        # Project to image
        u = self.fx * (Xc / Zc) + self.cx
        v = self.fy * (Yc / Zc) + self.cy

        # Keep only points in image bounds
        in_img = (u >= 0) & (u < self.img_w) & (v >= 0) & (v < self.img_h)
        u = u[in_img]
        v = v[in_img]
        Zc = Zc[in_img]
        pts_ego_front = pts_ego_front[in_img]

        if u.size == 0:
            return

        # Build fused output
        out = Float32MultiArray()
        out.data = []

        for det in det_msg.detections:
            if len(det.results) == 0:
                continue

            # YOLO class + score
            cls_id = float(int(det.results[0].hypothesis.class_id))
            score = float(det.results[0].hypothesis.score)

            # bbox from vision_msgs BoundingBox2D (center + size)
            cx = float(det.bbox.center.position.x)
            cy = float(det.bbox.center.position.y)
            sx = float(det.bbox.size_x)
            sy = float(det.bbox.size_y)

            x1 = (cx - sx / 2.0) - self.bbox_pixel_margin
            y1 = (cy - sy / 2.0) - self.bbox_pixel_margin
            x2 = (cx + sx / 2.0) + self.bbox_pixel_margin
            y2 = (cy + sy / 2.0) + self.bbox_pixel_margin

            # Associate projected lidar points inside bbox
            inside = (u >= x1) & (u <= x2) & (v >= y1) & (v <= y2)
            if np.count_nonzero(inside) < self.min_points_in_bbox:
                # Not enough points -> skip (or publish NaNs if you prefer)
                continue

            pts_obj_ego = pts_ego_front[inside]
            z_obj = Zc[inside]  # forward depth in camera optical (meters)

            # Robust depth filtering by percentile
            lo = np.percentile(z_obj, self.depth_percentile_low)
            hi = np.percentile(z_obj, self.depth_percentile_high)
            keep = (z_obj >= lo) & (z_obj <= hi)

            if np.count_nonzero(keep) < max(3, self.min_points_in_bbox // 3):
                continue

            pts_obj_ego = pts_obj_ego[keep]
            z_obj = z_obj[keep]

            # Estimate obstacle position in ego frame: median of associated points
            pos_ego = np.median(pts_obj_ego, axis=0)  # [X,Y,Z] in ego frame
            rng = float(np.linalg.norm(pos_ego))      # range from ego origin (approx)

            out.data.extend([
                cls_id, score,
                float(pos_ego[0]), float(pos_ego[1]), float(pos_ego[2]),
                rng
            ])

        if len(out.data) > 0:
            self.fused_pub.publish(out)

    # ----------------------------
    # Helpers
    # ----------------------------
    def pointcloud2_to_xyz(self, cloud_msg: PointCloud2):
        # Read x,y,z from PointCloud2
        points = []
        for p in point_cloud2.read_points(cloud_msg, field_names=("x", "y", "z"), skip_nans=True):
            points.append([p[0], p[1], p[2]])
        if len(points) == 0:
            return None
        return np.array(points, dtype=np.float32)


def main(args=None):
    rclpy.init(args=args)
    node = CarlaFusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
