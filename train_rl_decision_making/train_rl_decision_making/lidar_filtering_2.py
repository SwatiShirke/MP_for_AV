#!/usr/bin/env python3

"""
CARLA LiDAR live plotting + simple obstacle detection demo

What it does:
- Spawns ego vehicle
- Spawns obstacle vehicle ahead of ego at configurable x distance
- Attaches LiDAR to ego
- Displays live top-down LiDAR points in a pygame window
- Marks points in a forward detection zone
- Prints nearest obstacle distance estimate in front sector

Tested conceptually for CARLA 0.9.x Python API style.
"""

import glob
import os
import sys
import time
import math
import queue
import weakref

import numpy as np
import pygame

# =============================================================================
# Try to import CARLA
# =============================================================================
try:
    sys.path.append(
        glob.glob(
            os.path.expanduser("~/CARLA_*/PythonAPI/carla/dist/carla-*%d.%d-%s.egg")
            % (
                sys.version_info.major,
                sys.version_info.minor,
                "win-amd64" if os.name == "nt" else "linux-x86_64",
            )
        )[0]
    )
except IndexError:
    pass

import carla  # noqa: E402


# =============================================================================
# Config
# =============================================================================
HOST = "127.0.0.1"
PORT = 2000
TIMEOUT = 10.0

MAP_NAME = "Town03"

EGO_BLUEPRINT = "vehicle.mini.cooper"
OBS_BLUEPRINT = "vehicle.mini.cooper"

OBSTACLE_DISTANCE_METERS = 20.0  # obstacle ahead of ego
SPAWN_Z_LIFT = 0.5

USE_SYNCHRONOUS_MODE = True
FIXED_DELTA_SECONDS = 0.05  # 20 FPS simulation

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_TITLE = "CARLA LiDAR Live Plot"

# Visualization scale: meters -> pixels
PIXELS_PER_METER = 12.0

# LiDAR settings
LIDAR_RANGE = 40.0
LIDAR_CHANNELS = 32
LIDAR_POINTS_PER_SECOND = 120000
LIDAR_ROTATION_FREQUENCY = 20.0
LIDAR_UPPER_FOV = 10.0
LIDAR_LOWER_FOV = -30.0

# LiDAR mount on ego
LIDAR_X = 0.0
LIDAR_Y = 0.0
LIDAR_Z = 2.5

# Detection zone in ego/lidar frame
FRONT_X_MIN = 0.0
FRONT_X_MAX = 25.0
FRONT_Y_ABS_MAX = 2.5
FRONT_Z_MIN = -2.0
FRONT_Z_MAX = 2.0


# =============================================================================
# Utility
# =============================================================================
def get_actor_blueprint(world, bp_id):
    bp_lib = world.get_blueprint_library()
    bp = bp_lib.find(bp_id)
    if bp is None:
        raise RuntimeError(f"Blueprint not found: {bp_id}")
    if bp.has_attribute("role_name"):
        bp.set_attribute("role_name", "hero")
    return bp


def pick_spawn_transform(world):
    spawn_points = world.get_map().get_spawn_points()
    if not spawn_points:
        raise RuntimeError("No spawn points available in this map.")
    return spawn_points[0]


def make_obstacle_transform_ahead(base_transform, distance_ahead):
    """
    Create a transform ahead of base_transform in its forward direction.
    """
    yaw_rad = math.radians(base_transform.rotation.yaw)
    forward = carla.Vector3D(x=math.cos(yaw_rad), y=math.sin(yaw_rad), z=0.0)

    new_loc = carla.Location(
        x=base_transform.location.x + forward.x * distance_ahead,
        y=base_transform.location.y + forward.y * distance_ahead,
        z=base_transform.location.z + SPAWN_Z_LIFT,
    )

    return carla.Transform(new_loc, base_transform.rotation)


# =============================================================================
# LiDAR callback handler
# =============================================================================
class LidarProcessor:
    def __init__(self):
        self.queue = queue.Queue(maxsize=5)
        self.latest_points = None

    @staticmethod
    def _parse_lidar(raw_data):
        """
        CARLA LiDAR raw_data is float32 array of [x, y, z, intensity] repeated.
        """
        pts = np.frombuffer(raw_data, dtype=np.float32)
        pts = np.reshape(pts, (-1, 4))
        return pts

    @staticmethod
    def sensor_callback(weak_self, lidar_data):
        self = weak_self()
        if not self:
            return

        points = self._parse_lidar(lidar_data.raw_data)

        # Keep only latest frame
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break

        try:
            self.queue.put_nowait(points)
        except queue.Full:
            pass

    def update(self):
        try:
            self.latest_points = self.queue.get_nowait()
        except queue.Empty:
            pass
        return self.latest_points


# =============================================================================
# Visualization and detection
# =============================================================================
class LidarDisplay:
    def __init__(self, width, height, ppm):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.ppm = ppm
        self.center = np.array([width // 2, height // 2], dtype=np.int32)

        self.font = pygame.font.SysFont("Arial", 20)

    def world_to_screen(self, x, y):
        """
        Ego/lidar frame to top-down display:
        x forward, y right in CARLA vehicle frame
        We render:
        - forward up on screen
        - right to screen right
        """
        px = self.center[0] + int(y * self.ppm)
        py = self.center[1] - int(x * self.ppm)
        return px, py

    def draw_grid(self):
        self.screen.fill((0, 0, 0))

        # # X-axis (horizontal → right)
        # pygame.draw.line(
        #    self.screen,
        #    (255, 0, 0),
        #    (0, 0),
        #    (self.width, 0),
        #    2,
        # )
        
        # #Y-axis (vertical → down)
        # pygame.draw.line(
        #    self.screen,
        #    (0, 0, 255),
        #    (0, 0),
        #    (0, self.height),
        #    2,
        # )

        font = self.font

        # Labels
        self.screen.blit(font.render("Screen X →", True, (255, 0, 0)), (50, 5))
        self.screen.blit(font.render("Screen Y ↓", True, (0, 0, 255)), (5, 50))

        # Grid every 5 m
        for m in range(-40, 45, 5):
            # vertical lines (constant y)
            p1 = self.world_to_screen(-40, m)
            p2 = self.world_to_screen(40, m)
            pygame.draw.line(self.screen, (40, 40, 40), p1, p2, 1)

            # horizontal lines (constant x)
            p3 = self.world_to_screen(m, -40)
            p4 = self.world_to_screen(m, 40)
            pygame.draw.line(self.screen, (40, 40, 40), p3, p4, 1)

        # Ego marker
        pygame.draw.circle(self.screen, (0, 255, 0), self.center, 6)

        # Vehicle heading line
        pygame.draw.line(
            self.screen,
            (0, 255, 0),
            self.center,
            (self.center[0], self.center[1] - 25),
            2,
        )

        # Front detection box
        corners = [
            self.world_to_screen(FRONT_X_MIN, -FRONT_Y_ABS_MAX),
            self.world_to_screen(FRONT_X_MIN, FRONT_Y_ABS_MAX),
            self.world_to_screen(FRONT_X_MAX, FRONT_Y_ABS_MAX),
            self.world_to_screen(FRONT_X_MAX, -FRONT_Y_ABS_MAX),
        ]
        pygame.draw.polygon(self.screen, (255, 255, 0), corners, 2)

    def draw_points(self, points):
        if points is None or len(points) == 0:
            return None, 0

        xyz = points[:, :3]
        x = xyz[:, 0]
        y = xyz[:, 1]
        z = xyz[:, 2]

        # Keep within range
        mask = np.sqrt(x * x + y * y) <= LIDAR_RANGE
        xyz = xyz[mask]
        x = xyz[:, 0]
        y = xyz[:, 1]
        z = xyz[:, 2]

        # Front detection zone
        front_mask = (
            (x >= FRONT_X_MIN) &
            (x <= FRONT_X_MAX) &
            (np.abs(y) <= FRONT_Y_ABS_MAX) &
            (z >= FRONT_Z_MIN) &
            (z <= FRONT_Z_MAX)
        )

        nearest_distance = None
        num_detected = int(np.sum(front_mask))
        if num_detected > 0:
            d = np.sqrt(x[front_mask] ** 2 + y[front_mask] ** 2 + z[front_mask] ** 2)
            nearest_distance = float(np.min(d))

        # Draw points
        for i in range(len(xyz)):
            px, py = self.world_to_screen(x[i], y[i])

            if 0 <= px < self.width and 0 <= py < self.height:
                if front_mask[i]:
                    color = (255, 60, 60)  # detected region points
                    radius = 2
                else:
                    color = (180, 180, 255)
                    radius = 1
                pygame.draw.circle(self.screen, color, (px, py), radius)

        return nearest_distance, num_detected

    def draw_text(self, nearest_distance, num_detected):
        lines = [
            f"Detected front points: {num_detected}",
            f"Nearest front obstacle distance: "
            f"{nearest_distance:.2f} m" if nearest_distance is not None else
            "Nearest front obstacle distance: None"
        ]

        if nearest_distance is not None and nearest_distance < 20.0:
            lines.append("ALERT: obstacle ahead")

        y = 10
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (10, y))
            y += 24

    def render(self, points):
        self.draw_grid()
        nearest_distance, num_detected = self.draw_points(points)
        self.draw_text(nearest_distance, num_detected)
        pygame.display.flip()
        self.clock.tick(30)

        return nearest_distance, num_detected


# =============================================================================
# Main
# =============================================================================
def main():
    actor_list = []
    original_settings = None

    client = carla.Client(HOST, PORT)
    client.set_timeout(TIMEOUT)

    world = client.get_world()

    try:
        traffic_manager = client.get_trafficmanager()
        traffic_manager.set_synchronous_mode(USE_SYNCHRONOUS_MODE)

        if USE_SYNCHRONOUS_MODE:
            original_settings = world.get_settings()
            settings = world.get_settings()
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = FIXED_DELTA_SECONDS
            world.apply_settings(settings)

        # Spawn ego
        ego_transform = pick_spawn_transform(world)
        ego_bp = get_actor_blueprint(world, EGO_BLUEPRINT)
        ego = world.spawn_actor(ego_bp, ego_transform)
        actor_list.append(ego)
        ego.set_autopilot(False)

        # Spawn obstacle vehicle ahead
        obstacle_transform = make_obstacle_transform_ahead(ego_transform, OBSTACLE_DISTANCE_METERS)
        obs_bp = get_actor_blueprint(world, OBS_BLUEPRINT)
        obstacle = world.try_spawn_actor(obs_bp, obstacle_transform)

        if obstacle is None:
            # Small fallback shift
            obstacle_transform.location.y += 2.0
            obstacle = world.try_spawn_actor(obs_bp, obstacle_transform)

        if obstacle is None:
            raise RuntimeError("Could not spawn obstacle vehicle.")
        actor_list.append(obstacle)
        obstacle.set_autopilot(False)
        obstacle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))

        # Spawn LiDAR
        lidar_bp = world.get_blueprint_library().find("sensor.lidar.ray_cast")
        lidar_bp.set_attribute("range", str(LIDAR_RANGE))
        lidar_bp.set_attribute("channels", str(LIDAR_CHANNELS))
        lidar_bp.set_attribute("points_per_second", str(LIDAR_POINTS_PER_SECOND))
        lidar_bp.set_attribute("rotation_frequency", str(LIDAR_ROTATION_FREQUENCY))
        lidar_bp.set_attribute("upper_fov", str(LIDAR_UPPER_FOV))
        lidar_bp.set_attribute("lower_fov", str(LIDAR_LOWER_FOV))
        lidar_bp.set_attribute("sensor_tick", "0.0")

        lidar_transform = carla.Transform(carla.Location(x=LIDAR_X, y=LIDAR_Y, z=LIDAR_Z))
        lidar = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego)
        actor_list.append(lidar)

        processor = LidarProcessor()
        weak_processor = weakref.ref(processor)
        lidar.listen(lambda data: LidarProcessor.sensor_callback(weak_processor, data))

        display = LidarDisplay(WINDOW_WIDTH, WINDOW_HEIGHT, PIXELS_PER_METER)

        print("Running LiDAR live plot. Press ESC or close window to quit.")

        while True:
            if USE_SYNCHRONOUS_MODE:
                world.tick()
            else:
                world.wait_for_tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            points = processor.update()
            nearest_distance, num_detected = display.render(points)

            if nearest_distance is not None and num_detected > 5:
                print(f"[DETECTION] nearest front obstacle ≈ {nearest_distance:.2f} m")

    finally:
        print("Cleaning up actors...")
        for actor in actor_list:
            if actor is not None:
                actor.destroy()

        if original_settings is not None:
            world.apply_settings(original_settings)

        pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.")