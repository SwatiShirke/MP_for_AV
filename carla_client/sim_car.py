import carla
import pygame
import numpy as np
import time
from scipy.interpolate import interp2d, griddata
import pandas as pd
from matplotlib import pyplot as plt
import csv

# Pygame init
pygame.init()
display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
max_velocity = 30
max_pedal = 1
max_brake = 1
vel_steps = 20
pedal_steps = 20
brake_steps = 20
# Keep sensors alive until cleanup
active_sensors = []

def camera_callback(image, data_dict):
    """Convert CARLA image to Pygame surface"""
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))[:, :, :3]  # Take RGB
    array = array[:, :, ::-1]  # Convert BGR to RGB
    data_dict['surface'] = pygame.surfarray.make_surface(array.swapaxes(0, 1))

def spawn_vehicle(world):
    """Spawn Mini Cooper and attach RGB camera"""
    blueprint_library = world.get_blueprint_library()

    vehicle_bp = blueprint_library.filter('vehicle.mini.cooper')[0]
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(display_width))
    camera_bp.set_attribute('image_size_y', str(display_height))
    camera_bp.set_attribute('fov', '90')

    camera_transform = carla.Transform(
        carla.Location(x=-5.0, z=2.4),
        carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0)
    )
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

    data = {'surface': None}
    camera.listen(lambda image: camera_callback(image, data))

    # Keep strong reference so it won't be GC'd
    active_sensors.append(camera)

    return vehicle, camera, data

def reset_vehicle(world, vehicle):
    spawn_point = world.get_map().get_spawn_points()[0]
    # Move vehicle back to initial spawn location
    vehicle.set_transform(spawn_point)
    # Give the simulator a short moment to process the move
    time.sleep(0.1)


def forward_speed(vehicle):
    vel = vehicle.get_velocity()
    trans = vehicle.get_transform()
    fwd = trans.get_forward_vector()
    return vel.x * fwd.x + vel.y * fwd.y 

def forward_accel(vehicle):
    forward = vehicle.get_transform().get_forward_vector()
    accel = vehicle.get_acceleration()
    return accel.x * forward.x + accel.y * forward.y

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    velocities = np.linspace(0, max_velocity, vel_steps) #np.array([30.00]) 
    pedals = np.linspace(0, max_pedal, pedal_steps) #np.array([1.0])
    brakes =  np.linspace(0, max_brake, brake_steps)
    filpath = 'pedal_map_data.xlsx'
    # Clear the file before starting calculations
    with open(filpath, "w") as f:
        f.write("vel,pedal,accel\n")  # optional header
    vehicle, camera, data = spawn_vehicle(world)
    vehicle.set_autopilot(False)
    vel_list = []
    pedal_list = []
    accel_list = []
    
    for initial_v in velocities:
        #pedal logic
        for pedal in pedals:    
            print(f"Running case: initial_v ={initial_v} m/s, pedal={pedal}")
            #spawn_point = world.get_map().get_spawn_points()[0] 
            spawn_point = carla.Transform( carla.Location(x=-115, y=24.471010, z=0.600000),
                                                carla.Rotation(pitch=0.0, yaw=0.159198, roll=0.0)
                                               )
            vehicle.set_transform(spawn_point)
            # Ensure actors are ready
            world.tick()

            start_time = time.time()
            acceleration = 0
            while True:
                try:
                    world.wait_for_tick(2.0)  # FIXED: use seconds

                    if initial_v == 0:
                        vehicle.apply_control(carla.VehicleControl(throttle=0.0))
                    else:
                        vehicle.apply_control(carla.VehicleControl(throttle= 1.0))

                    velocity = forward_speed(vehicle)

                    if data['surface']:
                        display.blit(data['surface'], (0, 0))
                        pygame.display.flip()

                    if velocity >= initial_v:
                        break
                
                    
                except Exception as e:
                    print(f"[ERROR] Failed to apply control at main stage: {e}")
                    break

            try:
                vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))
                time.sleep(0.5)
                vehicle.apply_control(carla.VehicleControl(throttle=pedal,brake= 0.0))
                time.sleep(0.2)
                acceleration = forward_accel(vehicle)
                print(f"Acceleration: {acceleration:.2f} m/s²")
                vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
                vehicle.set_target_velocity(carla.Vector3D(0, 0, 0))
                vehicle.set_target_angular_velocity(carla.Vector3D(0, 0, 0))
            except Exception as e:
                print(f"[ERROR] Failed to apply control at main stage: {e}")
                continue

            # After computing acceleration:
            vel_list.append(initial_v)
            pedal_list.append(pedal)
            accel_list.append(acceleration)

             #save data
            with open(filpath, mode = 'a' , newline='') as f:
                writer = csv.writer(f)
                writer.writerow([initial_v, pedal, acceleration]) 
        
        #brake logic
        for brake in brakes:
            print(f"Running case: initial_v ={initial_v} m/s, brake={brake}")
            spawn_point = carla.Transform( carla.Location(x=-115.0, y=24.471010, z=0.600000),
                                                carla.Rotation(pitch=0.0, yaw=0.159198, roll=0.0)
                                                )
            
            #spawn_point = world.get_map().get_spawn_points()[0] 
            #print(spawn_point)
            vehicle.set_transform(spawn_point)
            # Ensure actors are ready
            world.tick()

            start_time = time.time()
            acceleration = 0
            while True:
                try:
                    world.wait_for_tick(2.0)  # FIXED: use seconds

                    if initial_v == 0:
                        vehicle.apply_control(carla.VehicleControl(throttle=0.0))
                    else:
                        vehicle.apply_control(carla.VehicleControl(throttle= 1.0))

                    velocity = forward_speed(vehicle)

                    if data['surface']:
                        display.blit(data['surface'], (0, 0))
                        pygame.display.flip()

                    if velocity >= initial_v:
                        break
                        
                    
                except Exception as e:
                        print(f"[ERROR] Failed to apply control at main stage: {e}")
                        break
            

            try:
                vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))
                time.sleep(0.5)
                vel_here = forward_speed(vehicle)
                print("vel here", vel_here )
                vehicle.apply_control(carla.VehicleControl(throttle= 0, brake=brake))
                time.sleep(0.2)
                acceleration = forward_accel(vehicle)
                print(f"Acceleration: {acceleration:.2f} m/s²")
                vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
                vehicle.set_target_velocity(carla.Vector3D(0, 0, 0))
                vehicle.set_target_angular_velocity(carla.Vector3D(0, 0, 0))
            except Exception as e:
                print(f"[ERROR] Failed to apply control at main stage: {e}")
                continue

            # After computing acceleration:
            vel_list.append(initial_v)
            pedal_list.append(-1 * brake)
            accel_list.append(acceleration)

            #save data
            with open(filpath, mode = 'a' , newline='') as f:
                writer = csv.writer(f)
                writer.writerow([initial_v, -1 * brake, acceleration]) 



    # Cleanup properly
    camera.stop()
    if camera in active_sensors:
        active_sensors.remove(camera)
    camera.destroy()
    vehicle.destroy()

    # # After loops:
    df = pd.DataFrame({
        'velocity': vel_list,
        'pedal': pedal_list,
        'acceleration': accel_list
    })

    #plot
    plt.figure(figsize=(10, 6))
    for pedal in pedals:
        subset = df[df['pedal'] == pedal]
        plt.plot(np.array(subset['velocity']),np.array(subset['acceleration']), label=f'Pedal={pedal:.2f}') 
    plt.xlabel('Initial Velocity (m/s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('Acceleration vs Initial Velocity for different Pedal Values')
    plt.legend()
    plt.grid(True)
    plt.show()

    #df.to_excel('pedal_map_data.xlsx', index=False)
    print("Data saved to pedal_map_data.xlsx")



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulation interrupted.")


