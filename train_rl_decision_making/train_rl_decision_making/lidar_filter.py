import carla
from collections import deque
import time
import numpy as np
from matplotlib import pyplot as plt

HOST = "localhost"
PORT = 2000
TIMEOUT = 10.0
BP = "vehicle.mini.cooper"
fwd_dist = 10

# Plot / sensor settings
LIDAR_RANGE = 40.0
POINTS_PER_SECOND = 150000
CHANNELS = 128
ROTATION_FREQUENCY = 50.0
UPPER_FOV = 30.0
LOWER_FOV = -30.0
Buffer_size = 15


class LidarProcessing:
    def __init__(self, vehicle, world):
        self.ego_vehicle = vehicle
        self.buffer = deque(maxlen=Buffer_size)

        def lidar_callback(data):
            points = np.frombuffer(data.raw_data, dtype=np.float32)
            points = points.reshape(-1, 4)
            points = points[:, 0:3]

            current_tx = self.ego_vehicle.get_transform()
            location = (
                current_tx.location.x,
                current_tx.location.y,
                current_tx.rotation.yaw,
            )

            self.buffer.append([location, points])

        blueprint_library = world.get_blueprint_library()
        lidar_bp = blueprint_library.find("sensor.lidar.ray_cast")
        lidar_bp.set_attribute("range", str(LIDAR_RANGE))
        lidar_bp.set_attribute("channels", str(CHANNELS))
        lidar_bp.set_attribute("points_per_second", str(POINTS_PER_SECOND))
        lidar_bp.set_attribute("rotation_frequency", str(ROTATION_FREQUENCY))
        lidar_bp.set_attribute("upper_fov", str(UPPER_FOV))
        lidar_bp.set_attribute("lower_fov", str(LOWER_FOV))

        lidar_transform = carla.Transform(carla.Location(x=0.0, z=2.5))
        self.lidar_sensor = world.spawn_actor(
            lidar_bp, lidar_transform, attach_to=self.ego_vehicle
        )
        self.lidar_sensor.listen(lidar_callback)

    def save_BEV(self):
        """iterate over last frames, convert to current ego frame and create a BEV"""
        print("inside save_BEV")

        if len(self.buffer) != Buffer_size:
            return 0

        all_data_points = []

        ego_location, ego_data = self.buffer[-1]
        T_w_ego_current = self.get_transform(ego_location)
        T_ego_current_w = np.linalg.inv(T_w_ego_current)

        for i in range(Buffer_size):
            location, data_points = self.buffer[i]
            T_w_ego_i = self.get_transform(location)
            T_current_i = T_ego_current_w @ T_w_ego_i

            ones = np.ones((data_points.shape[0], 1))
            data_vec = np.column_stack((data_points, ones))
            tx_data_vec = (T_current_i @ data_vec.T).T

            all_data_points.append(tx_data_vec[:, 0:3])

        all_data_points = np.vstack(all_data_points)
        self.plot_bev_metric(all_data_points, "./lidar_bev.png")

    def plot_bev_metric(
        self,
        data_points,
        save_path,
        x_min=0.0,
        x_max=40.0,
        y_min=-20.0,
        y_max=20.0,
        z_min=-2.5,
        z_max=5.0,
    ):
        """
        Plot BEV directly in meters, without converting to pixels.
        data_points must already be in current ego frame.
        x = forward (meters)
        y = lateral (meters)
        z = height (meters)
        """

        if data_points is None or len(data_points) == 0:
            return None

        xyz = data_points[:, :3]

        x = xyz[:, 0]
        y = xyz[:, 1]
        z = xyz[:, 2]

        mask = (
            (x >= x_min) & (x <= x_max) &
            (y >= y_min) & (y <= y_max) &
            (z >= z_min) & (z <= z_max)
        )

        xyz = xyz[mask]
        if xyz.shape[0] == 0:
            print("No points after filtering")
            return None

        x = xyz[:, 0]   # forward in meters
        y = xyz[:, 1]   # lateral in meters

        plt.figure(figsize=(8, 8))
        plt.scatter(y, x, s=0.5)
        plt.xlim(y_min, y_max)
        plt.ylim(x_min, x_max)
        plt.xlabel("Lateral distance (m)")
        plt.ylabel("Forward distance (m)")
        plt.title("BEV in Ego Frame (meters)")
        plt.grid(True)
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()    
        return xyz

    def get_transform(self, location):
        x, y, yaw = location
        yaw = np.deg2rad(yaw)

        c_t, s_t = np.cos(yaw), np.sin(yaw)
        R_mat = np.array([
            [c_t, -s_t, 0],
            [s_t,  c_t, 0],
            [0,    0,   1]
        ])

        pos_vec = np.array([[x], [y], [0]])
        T_mat = np.column_stack((R_mat, pos_vec))
        T_mat = np.vstack((T_mat, np.array([[0, 0, 0, 1]])))

        return T_mat

    def destroy(self):
        self.lidar_sensor.stop()
        self.lidar_sensor.destroy()


def main():
    client = carla.Client(HOST, PORT)
    client.set_timeout(TIMEOUT)

    world = client.get_world()
    original_settings = world.get_settings()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(True)

    blueprint_library = world.get_blueprint_library()
    ego_bp = blueprint_library.find(BP)
    spawn_points = world.get_map().get_spawn_points()
    ego_transform = spawn_points[0]

    ego_vehicle = None
    obs_vehicle = None
    ego_lidar_processor = None

    try:
        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)
        if ego_vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle.")

        ego_lidar_processor = LidarProcessing(ego_vehicle, world)

        fwd_vec = ego_transform.get_forward_vector()
        obs_x = ego_transform.location.x + fwd_dist * fwd_vec.x
        obs_y = ego_transform.location.y + fwd_dist * fwd_vec.y
        obs_loc = carla.Location(x=obs_x, y=obs_y, z=0.0)
        # obs_transform = carla.Transform(obs_loc, ego_transform.rotation)
        # obs_vehicle = world.try_spawn_actor(ego_bp, obs_transform)

        while True:
            print("inside while")
            world.tick()
            ego_lidar_processor.save_BEV()
            time.sleep(0.01)

    finally:
        if ego_lidar_processor is not None:
            ego_lidar_processor.destroy()
        if ego_vehicle is not None:
            ego_vehicle.destroy()
        if obs_vehicle is not None:
            obs_vehicle.destroy()

        world.apply_settings(original_settings)


if __name__ == "__main__":
    main()