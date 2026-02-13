import carla
import random
import numpy as np
import cv2
import time

# ------------------ CONNECT ------------------
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# Make sure async mode (simpler for camera)
settings = world.get_settings()
settings.synchronous_mode = False
settings.fixed_delta_seconds = None
world.apply_settings(settings)

blueprint_library = world.get_blueprint_library()

# ------------------ SPAWN VEHICLE ------------------
vehicle_bp = blueprint_library.filter("vehicle.mini.cooper")

spawn_point = random.choice(world.get_map().get_spawn_points())
vehicle = world.spawn_actor(vehicle_bp, spawn_point)
vehicle.set_autopilot(True)

# ------------------ SPAWN CAMERA ------------------
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '800')
camera_bp.set_attribute('image_size_y', '600')
camera_bp.set_attribute('fov', '90')
camera_bp.set_attribute('sensor_tick', '0.05')  # 20 Hz

camera_transform = carla.Transform(
    carla.Location(x=1.5, z=2.4)
)

camera = world.spawn_actor(
    camera_bp,
    camera_transform,
    attach_to=vehicle
)

# ------------------ CAMERA CALLBACK ------------------
def process_image(image):
    img = np.frombuffer(image.raw_data, dtype=np.uint8)
    img = img.reshape((image.height, image.width, 4))
    img = img[:, :, :3]
    img = img[:, :, ::-1]  # BGR -> RGB

    cv2.imshow("CARLA Camera", img)
    cv2.waitKey(1)

camera.listen(process_image)

# ------------------ RUN LOOP ------------------
print("Vehicle and camera spawned. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nDestroying actors...")

finally:
    camera.stop()
    camera.destroy()
    vehicle.destroy()
    cv2.destroyAllWindows()
