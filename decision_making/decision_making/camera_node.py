import rclpy
from rclpy.node import Node

import carla
import numpy as np
import cv2
import math

from std_msgs.msg import Header
from sensor_msgs.msg import CameraInfo

# YOLOv8 (Ultralytics)
from ultralytics import YOLO

# 2D detections (standard ROS message)
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose, BoundingBox2D


class CarlaCameraYoloNode(Node):
    """
    Attaches a CARLA RGB camera to ego vehicle (role_name='hero'),
    runs YOLOv8 on the camera frames,
    publishes ONLY:
      - /camera/camera_info          sensor_msgs/CameraInfo
      - /perception/detections2d     vision_msgs/Detection2DArray

    No image publishing (lightweight).
    """

    def __init__(self):
        super().__init__('carla_camera_yolo_node')

        # -----------------------------
        # CARLA connection
        # -----------------------------
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()

        self.vehicle = None
        self.camera = None

        # -----------------------------
        # Ego vehicle + camera mount
        # -----------------------------
        self.role_name = "hero"

        # You requested roof camera at z=2.4
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.cam_z = 2.4
        self.cam_roll = 0.0
        self.cam_pitch = 0.0
        self.cam_yaw = 0.0

        # -----------------------------
        # Camera params
        # -----------------------------
        self.image_w = 1280
        self.image_h = 720
        self.fov = 90.0  # horizontal FOV (deg), CARLA uses horizontal

        # -----------------------------
        # YOLO
        # -----------------------------
        # Replace with your YOLOv8 lite model path/name
        # e.g. "yolov8n.pt" or "yolov8n.engine" etc.
        self.model_path = "yolov8n.pt"
        self.yolo = YOLO(self.model_path)

        # Optional tuning
        self.conf_thres = 0.25
        self.iou_thres = 0.45

        # If you only care about vehicles, you can filter by COCO ids:
        # car=2, motorcycle=3, bus=5, truck=7
        self.vehicle_class_ids = {2, 3, 5, 7}

        # -----------------------------
        # ROS publishers (ONLY these)
        # -----------------------------
        self.caminfo_pub = self.create_publisher(CameraInfo, '/camera/camera_info', 10)
        self.det_pub = self.create_publisher(Detection2DArray, '/perception/detections2d', 10)

        # Build CameraInfo once (intrinsics)
        self.camera_info_msg = self.build_camera_info()

        # Spawn camera
        self.get_vehicle(self.role_name)
        self.setup_camera()

        self.get_logger().info(
            f"Camera YOLO node initialized (publishing CameraInfo + detections only). Model={self.model_path}"
        )

    # -------------------------------------------------
    # Find ego vehicle
    # -------------------------------------------------

    def get_vehicle(self, role_name: str):
        vehicles = self.world.get_actors().filter('vehicle.*')
        for v in vehicles:
            if v.attributes.get('role_name') == role_name:
                self.vehicle = v
                self.get_logger().info(f"Found ego vehicle role_name='{role_name}', id={v.id}")
                return
        raise RuntimeError(f"Vehicle with role_name '{role_name}' not found! Spawn it first.")

    # -------------------------------------------------
    # Spawn + attach camera
    # -------------------------------------------------
    
    def setup_camera(self):
        bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        bp.set_attribute('image_size_x', str(self.image_w))
        bp.set_attribute('image_size_y', str(self.image_h))
        bp.set_attribute('fov', str(self.fov))

        cam_tf = carla.Transform(
            carla.Location(x=self.cam_x, y=self.cam_y, z=self.cam_z),
            carla.Rotation(roll=self.cam_roll, pitch=self.cam_pitch, yaw=self.cam_yaw)
        )

        self.camera = self.world.spawn_actor(bp, cam_tf, attach_to=self.vehicle)
        self.camera.listen(self.camera_callback)

        self.get_logger().info("Camera attached to ego vehicle")

    # -------------------------------------------------
    # CameraInfo (intrinsics) from CARLA horizontal FOV
    # -------------------------------------------------
    def build_camera_info(self) -> CameraInfo:
        fx = (self.image_w / 2.0) / math.tan(math.radians(self.fov) / 2.0)
        fy = fx  # assume square pixels
        cx = self.image_w / 2.0
        cy = self.image_h / 2.0

        msg = CameraInfo()
        msg.width = self.image_w
        msg.height = self.image_h

        # K (3x3)
        msg.k = [
            fx, 0.0, cx,
            0.0, fy, cy,
            0.0, 0.0, 1.0
        ]

        # P (3x4)
        msg.p = [
            fx, 0.0, cx, 0.0,
            0.0, fy, cy, 0.0,
            0.0, 0.0, 1.0, 0.0
        ]

        msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        msg.distortion_model = "plumb_bob"
        return msg

    # -------------------------------------------------
    # Camera callback (CARLA thread)
    # -------------------------------------------------
    def camera_callback(self, carla_img: carla.Image):
        # CARLA raw is BGRA uint8
        img = np.frombuffer(carla_img.raw_data, dtype=np.uint8).reshape(
            (carla_img.height, carla_img.width, 4)
        )
        bgr = img[:, :, :3]  # BGRA -> BGR
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        # Timestamp + frame_id for both CameraInfo and Detections
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = "camera"

        # Publish CameraInfo (small)
        caminfo = self.camera_info_msg
        caminfo.header = header
        self.caminfo_pub.publish(caminfo)

        # Run YOLO
        det_arr = self.run_yolo_and_build_msg(rgb, header)
        self.det_pub.publish(det_arr)

    # -------------------------------------------------
    # YOLO inference -> Detection2DArray
    # -------------------------------------------------
    def run_yolo_and_build_msg(self, rgb: np.ndarray, header: Header) -> Detection2DArray:
        det_arr = Detection2DArray()
        det_arr.header = header

        # Ultralytics inference
        results = self.yolo(rgb, imgsz = 896 , conf=self.conf_thres, iou=self.iou_thres, device='cpu', verbose=False)[0]


        if results.boxes is None:
            return det_arr

        # boxes: xyxy, conf, cls
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
            conf = float(box.conf[0].cpu().numpy())
            cls_id = int(box.cls[0].cpu().numpy())

            # Optional: keep only vehicle-like classes
            if cls_id not in self.vehicle_class_ids:
                continue

            det = Detection2D()
            det.header = header

            bbox = BoundingBox2D()

            # center is Pose2D in your vision_msgs
            bbox.center.position.x = (x1 + x2) / 2.0
            bbox.center.position.y = (y1 + y2) / 2.0
            #bbox.center.orientation.theta = 0.0
            bbox.size_x = (x2 - x1)
            bbox.size_y = (y2 - y1)            
            det.bbox = bbox


            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = str(cls_id)
            hyp.hypothesis.score = conf
            det.results.append(hyp)

            det_arr.detections.append(det)

        return det_arr

    # -------------------------------------------------
    # Cleanup
    # -------------------------------------------------
    def destroy(self):
        if self.camera is not None:
            try:
                self.camera.stop()
            except Exception:
                pass
            self.camera.destroy()
            self.camera = None


def main(args=None):
    rclpy.init(args=args)
    node = CarlaCameraYoloNode()

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
