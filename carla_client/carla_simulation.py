import carla
import pygame
import numpy as np
import sys
import time
import math

# ------------------ Utils ------------------
def draw_image(surface, image):
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    array = array[:, :, :3][:, :, ::-1]  # BGRA → RGB
    surface.blit(pygame.surfarray.make_surface(array.swapaxes(0, 1)), (0, 0))


def get_speed_kmh(vehicle):
    v = vehicle.get_velocity()
    return math.sqrt(v.x**2 + v.y**2 + v.z**2) * 3.6


# ------------------ Main ------------------
def main():
    pygame.init()
    WIDTH, HEIGHT = 1200, 800
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CARLA Ego–Obstacle Scenario")

    client = carla.Client("localhost", 2000)
    client.set_timeout(30.0)
    time.sleep(2)

    # ---- Load world ----
    try:
        world = client.load_world("Town10HD_Opt")
    except RuntimeError:
        world = client.load_world("Town03")

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    blueprint_library = world.get_blueprint_library()

    # ------------------ Ego Vehicle ------------------
    ego_bp = blueprint_library.find("vehicle.mini.cooper")
    ego_bp.set_attribute("role_name", "hero")
    ego_bp.set_attribute("ros_name", "ego_vehicle")

    ego_transform = carla.Transform(
        carla.Location(x=-64.644844, y=24.471010, z=0.6),
        carla.Rotation(yaw=0)
    )

    hero_vehicle = world.spawn_actor(ego_bp, ego_transform)
    hero_vehicle.set_autopilot(False)
    print("[INFO] Ego vehicle spawned")

    # ------------------ Obstacle Vehicle ------------------
    obs_bp = blueprint_library.find("vehicle.mini.cooper")
    obs_bp.set_attribute("role_name", "obstacle")

    obs_transform = carla.Transform(
        carla.Location(x=-50.644844, y=24.471010, z=0.6),
        carla.Rotation(yaw=180)
    )

    obstacle_vehicle = world.spawn_actor(obs_bp, obs_transform)
    obstacle_vehicle.set_autopilot(False)
    print("[INFO] Obstacle vehicle spawned")

    # ------------------ Camera ------------------
    cam_bp = blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x", str(WIDTH))
    cam_bp.set_attribute("image_size_y", str(HEIGHT))
    cam_bp.set_attribute("fov", "100")

    cam_transform = carla.Transform(carla.Location(x=-4, z=2.4))
    camera = world.spawn_actor(cam_bp, cam_transform, attach_to=hero_vehicle)

    camera_surface = pygame.Surface((WIDTH, HEIGHT))
    camera.listen(lambda img: draw_image(camera_surface, img))

    # ------------------ Telemetry ------------------
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    # ------------------ Ego motion detection ------------------
    spawn_time = time.time()
    ego_started = False
    obstacle_started = False
    ego_move_counter = 0

    SPAWN_SETTLE_TIME = 1.0       # seconds
    MIN_THROTTLE = 0.05
    MIN_SPEED = 1.0              # km/h
    REQUIRED_FRAMES = 10         # consecutive ticks

    print("[INFO] Simulation running")

    try:
        while True:
            world.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # -------- Ego telemetry --------
            ego_control = hero_vehicle.get_control()
            speed = get_speed_kmh(hero_vehicle)
            transform = hero_vehicle.get_transform()

            # -------- Robust ego intent detection --------
            if time.time() - spawn_time > SPAWN_SETTLE_TIME:
                if ego_control.throttle > MIN_THROTTLE and speed > MIN_SPEED:
                    ego_move_counter += 1
                else:
                    ego_move_counter = 0

                if ego_move_counter >= REQUIRED_FRAMES:
                    ego_started = True

            # -------- Start obstacle --------
            if ego_started and not obstacle_started:
                obstacle_vehicle.set_autopilot(True)
                obstacle_started = True
                print("[INFO] Ego intentionally moving → Obstacle activated")

            # -------- Visualization --------
            display.blit(camera_surface, (0, 0))

            info = [
                f"X: {transform.location.x:.2f}",
                f"Y: {transform.location.y:.2f}",
                f"Yaw: {transform.rotation.yaw:.1f}",
                f"Speed: {speed:.1f} km/h",
                f"Throttle: {ego_control.throttle:.2f}",
                f"Ego started: {ego_started}",
                f"Obstacle started: {obstacle_started}",
            ]

            y = 10
            for line in info:
                display.blit(font.render(line, True, (255, 255, 255)), (10, y))
                y += 28

            pygame.display.flip()
            clock.tick(30)

    finally:
        print("[INFO] Cleaning up")
        camera.stop()
        hero_vehicle.destroy()
        obstacle_vehicle.destroy()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
