import carla
import random
import time
import weakref
import numpy as np
import matplotlib.pyplot as plt


HOST = "localhost"
PORT = 2000
TIMEOUT = 10.0

# Plot / sensor settings
LIDAR_RANGE = 40.0
POINTS_PER_SECOND = 150000
CHANNELS = 128
ROTATION_FREQUENCY = 50.0
UPPER_FOV = 30.0
LOWER_FOV = -30.0

# Spawn settings
FRONT_DISTANCE_METERS = 20.0


class LidarCollector:
    def __init__(self):
        self.latest_points = None

    def callback(self, lidar_data):
        # raw_data layout for ray-cast lidar is float32 xyzI
        points = np.frombuffer(lidar_data.raw_data, dtype=np.float32)
        points = np.reshape(points, (-1, 4))
        self.latest_points = points.copy()


def main():
    client = carla.Client(HOST, PORT)
    client.set_timeout(TIMEOUT)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    actors_to_destroy = []

    original_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(True)

    try:
        spawn_points = world.get_map().get_spawn_points()
        if not spawn_points:
            raise RuntimeError("No spawn points found in the map.")

        # ---- Ego vehicle ----
        vehicle_bps = blueprint_library.filter("vehicle.*")
        ego_bp = random.choice(vehicle_bps)

        ego_transform = random.choice(spawn_points)
        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)
        if ego_vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle.")

        actors_to_destroy.append(ego_vehicle)

        # ---- Obstacle vehicle 10 m in front of ego ----
        obstacle_bp = random.choice(vehicle_bps)

        forward = ego_transform.get_forward_vector()
        obstacle_location = ego_transform.location + carla.Location(
            x=forward.x * FRONT_DISTANCE_METERS,
            y=forward.y * FRONT_DISTANCE_METERS,
            z=0.5,
        )

        obstacle_transform = carla.Transform(
            obstacle_location,
            ego_transform.rotation
        )

        obstacle_vehicle = world.try_spawn_actor(obstacle_bp, obstacle_transform)

        # If direct spawn fails, try a few farther distances
        if obstacle_vehicle is None:
            for d in [12.0, 15.0, 18.0]:
                obstacle_location = ego_transform.location + carla.Location(
                    x=forward.x * d,
                    y=forward.y * d,
                    z=0.5,
                )
                obstacle_transform = carla.Transform(
                    obstacle_location,
                    ego_transform.rotation
                )
                obstacle_vehicle = world.try_spawn_actor(obstacle_bp, obstacle_transform)
                if obstacle_vehicle is not None:
                    break

        if obstacle_vehicle is None:
            raise RuntimeError("Failed to spawn obstacle vehicle in front of ego.")

        actors_to_destroy.append(obstacle_vehicle)

        # Keep both stationary for easy LiDAR visualization
        ego_vehicle.set_autopilot(False)
        obstacle_vehicle.set_autopilot(False)

        # ---- LiDAR sensor attached to ego ----
        lidar_bp = blueprint_library.find("sensor.lidar.ray_cast")
        lidar_bp.set_attribute("range", str(LIDAR_RANGE))
        lidar_bp.set_attribute("channels", str(CHANNELS))
        lidar_bp.set_attribute("points_per_second", str(POINTS_PER_SECOND))
        lidar_bp.set_attribute("rotation_frequency", str(ROTATION_FREQUENCY))
        lidar_bp.set_attribute("upper_fov", str(UPPER_FOV))
        lidar_bp.set_attribute("lower_fov", str(LOWER_FOV))

        # Slightly above the roof
        lidar_transform = carla.Transform(carla.Location(x=0.0, z=2.5))
        lidar_sensor = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego_vehicle)
        actors_to_destroy.append(lidar_sensor)

        collector = LidarCollector()
        weak_collector = weakref.ref(collector)

        def lidar_callback(data):
            ref = weak_collector()
            if ref is not None:
                ref.callback(data)

        lidar_sensor.listen(lidar_callback)

        # ---- Matplotlib live plot ----
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 8))
        scat = ax.scatter([], [], s=1)
        ax.set_title("CARLA LiDAR Top View (ego frame)")
        ax.set_xlabel("X forward (m)")
        ax.set_ylabel("Y left/right (m)")
        ax.set_xlim(-LIDAR_RANGE, LIDAR_RANGE)
        ax.set_ylim(-LIDAR_RANGE, LIDAR_RANGE)
        ax.grid(True)

        print("Running. Close the plot window or press Ctrl+C to stop.")

        # Let sensor warm up a few ticks
        for _ in range(10):
            world.tick()

        while plt.fignum_exists(fig.number):
            world.tick()

            if collector.latest_points is not None and len(collector.latest_points) > 0:
                pts = collector.latest_points

                # CARLA LiDAR returns points in sensor coordinates.
                # For top view we plot x,y only.
                xy = pts[:, :2]

                # Keep only points in front of the ego for cleaner view (xy[:, 0] >= 0.0) &
                mask = (
                    (xy[:, 0] >= -LIDAR_RANGE/2) &
                    (xy[:, 0] <= LIDAR_RANGE/2) &
                    (xy[:, 1] >= -LIDAR_RANGE/2) &
                    (xy[:, 1] <= LIDAR_RANGE/2)
                )
                # xy = xy[mask]

                scat.set_offsets(xy)

            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            time.sleep(0.01)

    finally:
        print("Cleaning up actors...")
        for actor in actors_to_destroy:
            if actor is not None:
                try:
                    actor.destroy()
                except Exception:
                    pass

        traffic_manager.set_synchronous_mode(False)
        world.apply_settings(original_settings)
        plt.ioff()
        plt.close("all")


if __name__ == "__main__":
    main()