import carla
import time

client = carla.Client("localhost", 2000)
client.set_timeout(5.0)

while True:
    world = client.get_world()
    actors = world.get_actors()

    sensors = [a for a in actors if a.type_id.startswith("sensor.")]
    vehicles = [a for a in actors if a.type_id.startswith("vehicle.")]
    others = [a for a in actors if not (a.type_id.startswith("sensor.") or a.type_id.startswith("vehicle."))]

    print(f"Sensors: {len(sensors)}, Vehicles: {len(vehicles)}, Others: {len(others)}, Total: {len(actors)}")

    time.sleep(2)