import carla
import numpy as np
import threading
import queue
import time
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class CarlaLidarProcessor:
    def __init__(
        self,
        world,
        ego_vehicle,
        save_dir="lidar_output",
        x_min=-10.0,
        x_max=50.0,
        y_min=-20.0,
        y_max=20.0,
        z_min=-2.0,
        z_max=2.0,
        grid_resolution=0.5,
        min_distance=5.0,
    ):
        self.world = world
        self.ego_vehicle = ego_vehicle
        self.save_dir = save_dir

        # ROI
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.grid_resolution = grid_resolution
        self.min_distance = min_distance

        # grid size
        self.grid_w = int((self.x_max - self.x_min) / self.grid_resolution)
        self.grid_h = int((self.y_max - self.y_min) / self.grid_resolution)

        # latest processed data
        self.latest_points = None
        self.latest_grid = None

        # threading
        self.data_lock = threading.Lock()
        self.data_ready = threading.Event()
        self.stop_event = threading.Event()
        self.lidar_queue = queue.Queue(maxsize=8)
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)

        # sensor
        self.lidar = None

        os.makedirs(self.save_dir, exist_ok=True)

    # --------------------------------------------------
    # sensor setup
    # --------------------------------------------------
    def spawn_lidar(self):
        bp = self.world.get_blueprint_library().find("sensor.lidar.ray_cast")
        bp.set_attribute("range", "50")
        bp.set_attribute("channels", "64")
        bp.set_attribute("points_per_second", "50000")
        bp.set_attribute("rotation_frequency", "20")
        bp.set_attribute("upper_fov", "10")
        bp.set_attribute("lower_fov", "-30")
        bp.set_attribute("sensor_tick", "0.0")

        lidar_tf = carla.Transform(
            carla.Location(x=1.2, y=0.0, z=2.8),
            carla.Rotation()
        )

        self.lidar = self.world.spawn_actor(bp, lidar_tf, attach_to=self.ego_vehicle)
        self.lidar.listen(self._lidar_callback)

        self.worker_thread.start()
        print("[INFO] LiDAR spawned and worker thread started")

    # --------------------------------------------------
    # callback
    # --------------------------------------------------
    def _lidar_callback(self, data):
        if self.stop_event.is_set():
            return

        try:
            self.lidar_queue.put_nowait(data)
        except queue.Full:
            # drop oldest frame if queue is full
            try:
                _ = self.lidar_queue.get_nowait()
                self.lidar_queue.put_nowait(data)
            except queue.Empty:
                pass

    # --------------------------------------------------
    # worker thread
    # --------------------------------------------------
    def _worker_loop(self):
        while not self.stop_event.is_set():
            try:
                data = self.lidar_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            points = self._decode_lidar(data)
            points = self._filter_points(points)
            grid = self._build_occupancy_grid(points)

            with self.data_lock:
                self.latest_points = points
                self.latest_grid = grid

            self.data_ready.set()

    # --------------------------------------------------
    # decoding
    # --------------------------------------------------
    def _decode_lidar(self, data):
        """
        CARLA raw_data: [x, y, z, intensity] float32
        """
        pts = np.frombuffer(data.raw_data, dtype=np.float32).reshape(-1, 4)
        return pts[:, :3]  # keep x, y, z only

    # --------------------------------------------------
    # filtering
    # --------------------------------------------------
    def _filter_points(self, pts):
        if pts.shape[0] == 0:
            return pts

        # remove near ego/self reflections
        dist = np.sqrt(pts[:, 0] ** 2 + pts[:, 1] ** 2)
        pts = pts[dist > self.min_distance]

        # ROI filter
        pts = pts[
            (pts[:, 0] >= self.x_min) & (pts[:, 0] <= self.x_max) &
            (pts[:, 1] >= self.y_min) & (pts[:, 1] <= self.y_max) &
            (pts[:, 2] >= self.z_min) & (pts[:, 2] <= self.z_max)
        ]

        return pts

    # --------------------------------------------------
    # BEV occupancy / count grid
    # --------------------------------------------------
    def _build_occupancy_grid(self, pts):
        grid = np.zeros((self.grid_h, self.grid_w), dtype=np.float32)

        if pts.shape[0] == 0:
            return grid

        x_idx = ((pts[:, 0] - self.x_min) / self.grid_resolution).astype(np.int32)
        y_idx = ((pts[:, 1] - self.y_min) / self.grid_resolution).astype(np.int32)

        valid = (
            (x_idx >= 0) & (x_idx < self.grid_w) &
            (y_idx >= 0) & (y_idx < self.grid_h)
        )

        x_idx = x_idx[valid]
        y_idx = y_idx[valid]

        # point count per cell
        np.add.at(grid, (y_idx, x_idx), 1.0)

        # log normalization for RL / visualization
        grid = np.log1p(grid) / np.log(64.0)   # cap-ish normalization
        grid = np.clip(grid, 0.0, 1.0)

        return grid

    # --------------------------------------------------
    # getters
    # --------------------------------------------------
    def get_latest_points(self):
        with self.data_lock:
            if self.latest_points is None:
                return None
            return self.latest_points.copy()

    def get_latest_grid(self):
        with self.data_lock:
            if self.latest_grid is None:
                return None
            return self.latest_grid.copy()

    # --------------------------------------------------
    # saving
    # --------------------------------------------------
    def save_points_npy(self, filename="lidar_points.npy"):
        pts = self.get_latest_points()
        if pts is None:
            print("[WARN] No LiDAR points available")
            return
        path = os.path.join(self.save_dir, filename)
        np.save(path, pts)
        print(f"[INFO] Saved points: {path}")

    def save_grid_npy(self, filename="lidar_grid.npy"):
        grid = self.get_latest_grid()
        if grid is None:
            print("[WARN] No LiDAR grid available")
            return
        path = os.path.join(self.save_dir, filename)
        np.save(path, grid)
        print(f"[INFO] Saved grid: {path}")

    def save_grid_png(self, filename="lidar_grid.png"):
        grid = self.get_latest_grid()
        if grid is None:
            print("[WARN] No LiDAR grid available")
            return

        path = os.path.join(self.save_dir, filename)

        plt.figure(figsize=(8, 6))
        plt.imshow(
            grid,
            extent=(self.x_min, self.x_max, self.y_min, self.y_max),
            origin="lower",
            aspect="auto"
        )
        plt.scatter(0, 0, marker="x", s=100)
        plt.title("LiDAR BEV Occupancy Grid")
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.colorbar(label="Normalized occupancy")
        plt.grid()
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[INFO] Saved grid image: {path}")

    def save_points_scatter_png(self, filename="lidar_points.png"):
        pts = self.get_latest_points()
        if pts is None:
            print("[WARN] No LiDAR points available")
            return

        path = os.path.join(self.save_dir, filename)

        plt.figure(figsize=(8, 6))
        plt.scatter(pts[:, 0], pts[:, 1], s=2)
        plt.scatter(0, 0, marker="x", s=100)
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.title("Filtered LiDAR Points")
        plt.grid()
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[INFO] Saved point scatter: {path}")

    # --------------------------------------------------
    # cleanup
    # --------------------------------------------------
    def destroy(self):
        self.stop_event.set()

        if self.lidar is not None:
            try:
                self.lidar.stop()
            except Exception:
                pass
            try:
                self.lidar.destroy()
            except Exception:
                pass
            self.lidar = None

        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1.0)

        print("[INFO] LiDAR processor cleaned up")


# ==========================================================
# Example main
# ==========================================================
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
    lidar_processor = None

    try:
        ego_bp = blueprint_library.find("vehicle.mini.cooper")
        ego_bp.set_attribute("role_name", "hero")
        ego_transform = carla.Transform(
            carla.Location(x=-64.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=0)
        )

        obs_bp = blueprint_library.find("vehicle.mini.cooper")
        obs_bp.set_attribute("role_name", "observer")
        obs_transform1 = carla.Transform(
            carla.Location(x=-50.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=180)
        )

        # spawn_points = world.get_map().get_spawn_points()
        # if len(spawn_points) == 0:
        #     raise RuntimeError("No spawn points found")

        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)
        if ego_vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle")

        ego_vehicle.set_autopilot(False)
        print("[INFO] Ego vehicle spawned")
        ego_tf = ego_vehicle.get_transform()

        # forward direction of ego
        forward = ego_tf.get_forward_vector()
        
        # compute spawn location
        # obs_location = ego_tf.location + carla.Location(
        #     x=forward.x * 10.0,
        #     y=forward.y * 10.0,
        #     z=0.0
        # )
        
        # spawn_tf = carla.Transform(
        #     obs_location,
        #     ego_tf.rotation
        # )
       
        
        obs_vehicle = world.try_spawn_actor(obs_bp, obs_transform1)
        
        if obs_vehicle is None:
            raise RuntimeError("Failed to spawn observer vehicle")
        
        world.tick()

        lidar_processor = CarlaLidarProcessor(
            world=world,
            ego_vehicle=ego_vehicle,
            save_dir="lidar_output",
            x_min=-10.0,
            x_max=50.0,
            y_min=-20.0,
            y_max=20.0,
            z_min=-1.5,
            z_max=1.5,
            grid_resolution=0.5,
            min_distance=2.5,
        )

        lidar_processor.spawn_lidar()

        # let a few frames arrive
        for _ in range(20):
            world.tick()
            time.sleep(0.01)

        if not lidar_processor.data_ready.is_set():
            print("[WARN] No LiDAR data received")
            return

        lidar_processor.save_points_npy("frame_points.npy")
        lidar_processor.save_grid_npy("frame_grid.npy")
        lidar_processor.save_points_scatter_png("frame_points.png")
        lidar_processor.save_grid_png("frame_grid.png")

    finally:
        if lidar_processor is not None:
            lidar_processor.destroy()

        if ego_vehicle is not None:
            try:
                ego_vehicle.destroy()
            except Exception:
                pass

        world.apply_settings(original_settings)


if __name__ == "__main__":
    main()