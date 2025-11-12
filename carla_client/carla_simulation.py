import carla
import pygame
import numpy as np
import random
import sys
import time
import math

def draw_image(surface, image):
    """Convert CARLA image to a pygame surface."""
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    array = array[:, :, :3][:, :, ::-1]  # BGRA → RGB
    surface.blit(pygame.surfarray.make_surface(array.swapaxes(0, 1)), (0, 0))

def main():
    pygame.init()
    width, height = 1200, 800
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CARLA Mini Cooper Simulation")

    client = carla.Client("localhost", 2000)
    client.set_timeout(30.0)
    time.sleep(2)

    try:
        print("[INFO] Loading Town10HD_Opt ...")
        world = client.load_world("Town10HD_Opt")
    except RuntimeError:
        print("[WARN] Town10HD_Opt not found, loading Town03 instead ...")
        world = client.load_world("Town03")

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.find("vehicle.mini.cooper")
    vehicle_bp.set_attribute("role_name", "hero")
    vehicle_bp.set_attribute("ros_name", "ego_vehicle")
    spawn_points = world.get_map().get_spawn_points()
    if not spawn_points:
        raise RuntimeError("No spawn points available!")

    #ego_transform = carla.Transform(carla.Location(x=-110.96, y=50.69, z=0.6), carla.Rotation(yaw=180))
    ego_transform = carla.Transform(carla.Location(x=-108.96, y=51.69, z=0.6), carla.Rotation(yaw=180))
    hero_vehicle = world.spawn_actor(vehicle_bp, ego_transform)
    hero_vehicle.set_autopilot(False)
    print(f"[INFO] Hero vehicle spawned at: {ego_transform.location}")

    # Camera setup
    # camera_bp = blueprint_library.find("sensor.camera.rgb")
    # camera_bp.set_attribute("image_size_x", str(width))
    # camera_bp.set_attribute("image_size_y", str(height))
    # camera_bp.set_attribute("fov", "100")
    # cam_transform = carla.Transform(carla.Location(x=-4, z=2.4))
    # camera = world.spawn_actor(camera_bp, cam_transform, attach_to=hero_vehicle)
    # camera_surface = pygame.Surface((width, height))
    # camera.listen(lambda image: draw_image(camera_surface, image))

    # --- FONT setup for telemetry ---
    font = pygame.font.Font(None, 32)
    text_color = (0, 0, 0)  # white

    clock = pygame.time.Clock()
    running = True
    print("[INFO] Simulation running. Hero = manual control.")
    try:
        while running:
            world.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # --- Get vehicle telemetry ---
            transform = hero_vehicle.get_transform()
            location = transform.location
            yaw = transform.rotation.yaw
            control = hero_vehicle.get_control()
            velocity = hero_vehicle.get_velocity()
            speed = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2) * 3.6  # km/h

            # --- Prepare telemetry text ---
            # info_lines = [
            #     f"X: {location.x:.2f} m",
            #     f"Y: {location.y:.2f} m",
            #     f"Yaw: {yaw:.1f}°",
            #     f"Speed: {speed:.1f} km/h",
            #     f"Throttle: {control.throttle:.2f}",
            #     f"Brake: {control.brake:.2f}",
            #     f"Steer: {control.steer:.2f}"
            # ]

            # # --- Draw camera image first ---
            # display.blit(camera_surface, (0, 0))

            # # --- Render telemetry on top-left ---
            # y_offset = 10
            # for line in info_lines:
            #     text_surface = font.render(line, True, text_color)
            #     display.blit(text_surface, (10, y_offset))
            #     y_offset += 28

            # pygame.display.flip()
            clock.tick(30)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting simulation by user.")

    finally:
        # print("[INFO] Cleaning up actors...")
        # camera.stop()
        hero_vehicle.destroy()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
