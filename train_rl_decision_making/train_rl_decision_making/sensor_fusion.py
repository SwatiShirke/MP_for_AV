import carla
import numpy as np
import cv2
import math
import threading
import random
import time
import matplotlib
matplotlib.use("Agg")   # avoid Qt/xcb GUI crash
import matplotlib.pyplot as plt


class SensorFusion:
    """
    Camera + LiDAR + Collision sensor
    Thread-safe CARLA perception module for RL/testing
    """

    def __init__(
        self,
        world,
        min_distance,
        max_objects=10,
        ego_vehicle=None,
        x_max=50.0,
        y_max=20.0,
        x_min=-10.0,
        y_min=-20.0,
        grid_resolution=0.5
    ):
        self.world = world
        self.max_objects = max_objects
        self.min_distance = min_distance
        self.ego_vehicle = ego_vehicle

        self.x_max = x_max
        self.y_max = y_max
        self.x_min = x_min
        self.y_min = y_min
        self.grid_resolution = grid_resolution

        # -----------------------
        # Camera parameters
        # -----------------------
        self.image_w = 1280
        self.image_h = 720
        self.fov = 90.0

        self.cam_tf = carla.Transform(
            carla.Location(x=0.0, y=0.0, z=2.4),
            carla.Rotation()
        )

        # -----------------------
        # LiDAR parameters
        # -----------------------
        self.lidar_tf = carla.Transform(
            carla.Location(x=1.2, y=0.0, z=2.8)
        )

        # -----------------------
        # Camera intrinsics
        # -----------------------
        self.fx = (self.image_w / 2.0) / math.tan(math.radians(self.fov) / 2.0)
        self.fy = self.fx
        self.cx = self.image_w / 2.0
        self.cy = self.image_h / 2.0

        # -----------------------
        # Internal shared buffers
        # -----------------------
        self.rgb_img = None
        self.grid = None
        self.latest_lidar_points = None

        self.collision_happened = False
        self.actor_collided = None

        # -----------------------
        # Threading primitives
        # -----------------------
        self.rgb_lock = threading.Lock()
        self.lidar_lock = threading.Lock()
        self.collision_lock = threading.Lock()

        self.rgb_ready = threading.Event()
        self.lidar_ready = threading.Event()
        self.stop_event = threading.Event()

        # -----------------------
        # Sensor handles
        # -----------------------
        self.camera = None
        self.lidar = None
        self.collision_sensor = None

        self.setup()

    # =========================================================
    # Setup
    # =========================================================
    def setup(self):
        self._spawn_camera()
        self._spawn_lidar()
        self.spawn_collision_sensor()

    def _spawn_camera(self):
        bp = self.world.get_blueprint_library().find("sensor.camera.rgb")
        bp.set_attribute("role_name", "rl_sensor_camera")
        bp.set_attribute("image_size_x", str(self.image_w))
        bp.set_attribute("image_size_y", str(self.image_h))
        bp.set_attribute("fov", str(self.fov))
        bp.set_attribute("sensor_tick", "0.0")

        self.camera = self.world.spawn_actor(bp, self.cam_tf, attach_to=self.ego_vehicle)
        self.camera.listen(self._camera_callback)

    def _spawn_lidar(self):
        bp = self.world.get_blueprint_library().find("sensor.lidar.ray_cast")
        bp.set_attribute("role_name", "rl_sensor_lidar")
        bp.set_attribute("range", "50")
        bp.set_attribute("channels", "32")
        bp.set_attribute("points_per_second", "50000")
        bp.set_attribute("rotation_frequency", "20")
        bp.set_attribute("upper_fov", "10")
        bp.set_attribute("lower_fov", "-30")
        bp.set_attribute("sensor_tick", "0.0")

        self.lidar = self.world.spawn_actor(bp, self.lidar_tf, attach_to=self.ego_vehicle)
        self.lidar.listen(self._lidar_callback)

    def spawn_collision_sensor(self):
        bp = self.world.get_blueprint_library().find("sensor.other.collision")
        transform = carla.Transform(carla.Location(x=0.0, z=1.0))
        self.collision_sensor = self.world.spawn_actor(bp, transform, attach_to=self.ego_vehicle)
        self.collision_sensor.listen(self._on_collision)

    # =========================================================
    # Callbacks
    # =========================================================
    def _camera_callback(self, img):
        if self.stop_event.is_set():
            return

        arr = np.frombuffer(img.raw_data, dtype=np.uint8).reshape(
            (img.height, img.width, 4)
        )[:, :, :3]

        rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

        with self.rgb_lock:
            self.rgb_img = rgb.copy()

        self.rgb_ready.set()

    def _lidar_callback(self, data):
        if self.stop_event.is_set():
            return

        pts = np.frombuffer(data.raw_data, dtype=np.float32).reshape(-1, 4)[:, :3]
        dist = np.sqrt(pts[:,0]**2 + pts[:,1]**2)
        pts = pts[dist > self.min_distance]
        if pts.shape[0] == 0:
            return

        pts = pts[
            (pts[:, 0] >= self.x_min) & (pts[:, 0] <= self.x_max) &
            (pts[:, 1] >= self.y_min) & (pts[:, 1] <= self.y_max)
        ]

        grid_h = int((self.y_max - self.y_min) / self.grid_resolution)
        grid_w = int((self.x_max - self.x_min) / self.grid_resolution)
        grid = np.zeros((grid_h, grid_w), dtype=np.float32)

        for pt in pts:
            x_index = int((pt[0] - self.x_min) / self.grid_resolution)
            y_index = int((pt[1] - self.y_min) / self.grid_resolution)

            if 0 <= y_index < grid_h and 0 <= x_index < grid_w:
                grid[y_index, x_index] = 1.0

        with self.lidar_lock:
            self.latest_lidar_points = pts.copy()
            self.grid = grid

        self.lidar_ready.set()

    def _on_collision(self, event):
        if self.stop_event.is_set():
            return

        with self.collision_lock:
            self.collision_happened = True
            self.actor_collided = event.other_actor.type_id

    # =========================================================
    # Safe getters
    # =========================================================
    def get_rgb(self):  
        with self.rgb_lock:
            if self.rgb_img is None:
                return None
            return self.rgb_img.copy()

    def get_lidar_grid(self):
        with self.lidar_lock:
            if self.grid is None:
                return None
            return self.grid.copy()

    def save_camera_image(self, path):
        rgb = self.get_rgb()
        if rgb is not None:
            cv2.imwrite(path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            print(f"[INFO] Saved camera image to {path}")
        else:
            print("[WARN] No RGB image available to save")

    def get_collision_state(self):
        with self.collision_lock:
            return self.collision_happened, self.actor_collided

    def wait_for_data(self, timeout=2.0):
        rgb_ok = self.rgb_ready.wait(timeout=timeout)
        lidar_ok = self.lidar_ready.wait(timeout=timeout)
        return rgb_ok and lidar_ok

    # =========================================================
    # Plot / Save
    # =========================================================
    def plot_lidar_grid(self, save_path="lidar_grid.png"):
        grid = self.get_lidar_grid()
        if grid is None:
            print("[WARN] No LiDAR grid available yet")
            return

        plt.figure(figsize=(8, 6))
        plt.imshow(
            grid,
            extent=(self.x_min, self.x_max, self.y_min, self.y_max),
            origin="lower",
            aspect="auto"
        )
        plt.title("LiDAR Occupancy Grid")
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.colorbar(label="Occupancy")
        plt.grid()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[INFO] Saved LiDAR grid to {save_path}")

    # =========================================================
    # Placeholder state API
    # =========================================================
    def get_current_state(self, traj_waypoints=None, ego_state=None, step_count=0):
        rgb = self.get_rgb()
        grid = self.get_lidar_grid()
        collision_happened, actor_collided = self.get_collision_state()

        return {
            "rgb": rgb,
            "lidar_grid": grid,
            "traj_waypoints": traj_waypoints,
            "ego_state": ego_state,
            "step_count": step_count,
            "collision_happened": collision_happened,
            "actor_collided": actor_collided,
        }

    # =========================================================
    # Test code
    # =========================================================
    def spawn_vehicle_in_front(
        self,
        distance=15.0,
        lateral_offset=0.0,
        vehicle_filter="vehicle.*",
        autopilot=False
    ):
        blueprint_library = self.world.get_blueprint_library()
        vehicle_bps = blueprint_library.filter(vehicle_filter)
        if not vehicle_bps:
            raise RuntimeError("No vehicle blueprints found")

        bp = random.choice(vehicle_bps)

        ego_tf = self.ego_vehicle.get_transform()
        ego_loc = ego_tf.location
        ego_rot = ego_tf.rotation

        yaw_rad = math.radians(ego_rot.yaw)
        forward = carla.Vector3D(
            x=math.cos(yaw_rad),
            y=math.sin(yaw_rad),
            z=0.0
        )
        right = carla.Vector3D(
            x=-math.sin(yaw_rad),
            y=math.cos(yaw_rad),
            z=0.0
        )

        spawn_loc = ego_loc + forward * distance + right * lateral_offset
        spawn_loc.z += 0.1

        print("spawned location for obstacle vehicle", spawn_loc)

        spawn_tf = carla.Transform(
            spawn_loc,
            carla.Rotation(yaw=ego_rot.yaw)
        )

        vehicle = self.world.try_spawn_actor(bp, spawn_tf)
        if vehicle is None:
            print("[TEST] Failed to spawn vehicle (collision)")
            return None

        if autopilot:
            vehicle.set_autopilot(True)

        print(
            f"[TEST] Spawned vehicle id={vehicle.id} "
            f"at {distance:.1f} m ahead, lateral {lateral_offset:.1f} m"
        )
        return vehicle

    def test_fusion(self, num_vehicles=5):
        for _ in range(10):
            self.world.tick()

        ok = self.wait_for_data(timeout=2.0)
        if not ok:
            print("[WARN] Timed out waiting for sensor data")
            return

        state = self.get_current_state(step_count=10)

        print("[INFO] RGB available:", state["rgb"] is not None)
        print("[INFO] LiDAR grid available:", state["lidar_grid"] is not None)
        print("[INFO] Collision:", state["collision_happened"], state["actor_collided"])

        self.plot_lidar_grid("lidar_grid.png")

    # =========================================================
    # Cleanup
    # =========================================================
    def destroy(self):
        self.stop_event.set()

        sensors = [self.camera, self.lidar, self.collision_sensor]
        for sensor in sensors:
            if sensor is not None:
                try:
                    sensor.stop()
                except Exception:
                    pass

        for sensor in sensors:
            if sensor is not None:
                try:
                    sensor.destroy()
                except Exception:
                    pass

        self.camera = None
        self.lidar = None
        self.collision_sensor = None


def spawn_ego_vehicle(
    world,
    blueprint_filter="vehicle.tesla.model3",
    spawn_point=None,
    role_name="hero",
    autopilot=False
):
    bp_lib = world.get_blueprint_library()
    candidates = bp_lib.filter(blueprint_filter)
    if not candidates:
        raise RuntimeError(f"No vehicle blueprint matches '{blueprint_filter}'")

    bp = random.choice(candidates)
    bp.set_attribute("role_name", role_name)

    vehicle = world.try_spawn_actor(bp, spawn_point)
    if vehicle is None:
        raise RuntimeError("Failed to spawn ego vehicle (collision at spawn point)")

    vehicle.set_autopilot(autopilot)
    print(f"[EGO] Spawned ego vehicle at {spawn_point.location}")
    return vehicle


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    original_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    ego_vehicle = None
    obstacle_vehicle1 = None
    obstacle_vehicle2 = None
    obstacle_vehicle3 = None
    fusion = None

    try:
        ego_bp = blueprint_library.find("vehicle.mini.cooper")
        ego_bp.set_attribute("role_name", "hero")
        ego_bp.set_attribute("ros_name", "ego_vehicle")

        ego_transform = carla.Transform(
            carla.Location(x=-64.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=0)
        )

        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)
        if ego_vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle (collision at spawn point).")

        ego_vehicle.set_autopilot(False)
        print("[INFO] Ego vehicle spawned")

        obs_bp = blueprint_library.find("vehicle.mini.cooper")
        obs_bp.set_attribute("role_name", "obstacle")

        obs_transform1 = carla.Transform(
            carla.Location(x=-54.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=180)
        )
        obstacle_vehicle1 = world.try_spawn_actor(obs_bp, obs_transform1)
        if obstacle_vehicle1 is None:
            print("[WARN] Failed to spawn obstacle vehicle 1 (collision).")
        else:
            obstacle_vehicle1.set_autopilot(False)
            print("[INFO] Obstacle vehicle 1 spawned")

        obs_bp2 = blueprint_library.find("vehicle.mini.cooper")
        obs_bp2.set_attribute("role_name", "obstacle")

        obs_transform2 = carla.Transform(
            carla.Location(x=-52.4844, y=28.471010, z=0.6),
            carla.Rotation(yaw=180)
        )
        obstacle_vehicle2 = world.try_spawn_actor(obs_bp2, obs_transform2)
        if obstacle_vehicle2 is None:
            print("[WARN] Failed to spawn obstacle vehicle 2 (collision).")
        else:
            obstacle_vehicle2.set_autopilot(False)
            print("[INFO] Obstacle vehicle 2 spawned")

        obs_bp3 = blueprint_library.find("vehicle.mini.cooper")
        obs_bp3.set_attribute("role_name", "obstacle")

        obs_transform3 = carla.Transform(
            carla.Location(x=-52.4844, y=20.471010, z=0.6),
            carla.Rotation(yaw=180)
        )
        obstacle_vehicle3 = world.try_spawn_actor(obs_bp3, obs_transform3)
        if obstacle_vehicle3 is None:
            print("[WARN] Failed to spawn obstacle vehicle 3 (collision).")
        else:
            obstacle_vehicle3.set_autopilot(False)
            print("[INFO] Obstacle vehicle 3 spawned")

        world.tick()

        fusion = SensorFusion(
            world=world,
            ego_vehicle=ego_vehicle,
            min_distance=5.0
        )

        fusion.test_fusion(num_vehicles=5)

    finally:
        if fusion is not None:
            fusion.destroy()

        for v in [obstacle_vehicle1, obstacle_vehicle2, obstacle_vehicle3, ego_vehicle]:
            if v is not None:
                try:
                    v.destroy()
                except Exception:
                    pass

        world.apply_settings(original_settings)


if __name__ == "__main__":
    main()