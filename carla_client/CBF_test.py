import carla
import pygame
import numpy as np
import random
import sys
import time

def draw_image(surface, image):
    """Convert CARLA image to a pygame surface"""
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    array = array[:, :, :3][:, :, ::-1]  # BGRA → RGB
    surface.blit(pygame.surfarray.make_surface(array.swapaxes(0, 1)), (0, 0))

def main():
    # Initialize Pygame
    pygame.init()
    width, height = 800, 600
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CARLA Mini Cooper Autopilot")

    # Connect to CARLA
    client = carla.Client("localhost", 2000)
    client.set_timeout(30.0)
    time.sleep(2)  # allow server to start properly

    # Load Town10HD_Opt map
    print("[INFO] Loading Town10HD_Opt ...")
    world = client.load_world("Town10HD_Opt")

    # Enable synchronous mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    # Get blueprint library
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.find("vehicle.mini.cooper_s_2021")  # Mini Cooper
    vehicle_bp.set_attribute('role_name', 'hero')

    # Spawn the vehicle
    spawn_points = world.get_map().get_spawn_points()
    if not spawn_points:
        raise RuntimeError("No spawn points available!")
    spawn_point = random.choice(spawn_points)
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    print(f"[INFO] Mini Cooper spawned at: {spawn_point.location}")

    # Attach front RGB camera
    camera_bp = blueprint_library.find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", str(width))
    camera_bp.set_attribute("image_size_y", str(height))
    camera_bp.set_attribute("fov", "100")
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
    camera_surface = pygame.Surface((width, height))
    camera.listen(lambda image: draw_image(camera_surface, image))

    # Setup Traffic Manager
    tm = client.get_trafficmanager(8000)
    tm.set_synchronous_mode(True)
    tm.global_percentage_speed_difference(10.0)  # slightly slower
    tm.set_global_distance_to_leading_vehicle(2.5)

    # Enable autopilot
    vehicle.set_autopilot(True, tm.get_port())

    # Main loop
    clock = pygame.time.Clock()
    running = True
    print("[INFO] Autopilot started. Close the window to exit.")

    try:
        while running:
            world.tick()  # advance simulation
            tm.tick()     # update Traffic Manager

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            display.blit(camera_surface, (0, 0))
            pygame.display.flip()
            clock.tick(30)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting simulation by user.")

    finally:
        # Cleanup
        print("[INFO] Cleaning up actors...")
        camera.stop()
        vehicle.destroy()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
