import os
import rosbag2_py
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # Import ticker for formatting
from rclpy.serialization import deserialize_message
from nav_msgs.msg import Odometry, Path
from carla_msgs.msg import CarlaEgoVehicleControl
from std_msgs.msg import Float32  # Import Float32 for norm_error topic
import numpy as np
from vd_msgs.msg import VDPath

def read_vehicle_bag_data(bag_path):
    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
    reader.open(storage_options, converter_options)

    topics = [
        'global_path',
        '/carla/ego_vehicle/odometry',
        '/carla/ego_vehicle/vehicle_control_cmd',
        '/carla/ego_vehicle/waypoints',
        '/norm_error'  # Include norm_error topic
    ]
    topic_data = {topic: [] for topic in topics}

    while reader.has_next():
        topic_name, serialized_msg, t = reader.read_next()
        #print(topic_name, " ", t)
        
        # Convert nanoseconds to seconds
        time_sec = t * 1e-9

        if topic_name in topics:
            if topic_name == 'global_path':
                msg = deserialize_message(serialized_msg, VDPath) 
                topic_data[topic_name].append((time_sec, msg.x_val, msg.y_val))

            if topic_name == '/carla/ego_vehicle/odometry':
                msg = deserialize_message(serialized_msg, Odometry)
                topic_data[topic_name].append((time_sec, msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z,
                                               msg.pose.pose.orientation.x,  # Yaw angle
                                               msg.twist.twist.linear.x))  # Longitudinal velocity
            elif topic_name == '/carla/ego_vehicle/vehicle_control_cmd':
                msg = deserialize_message(serialized_msg, CarlaEgoVehicleControl)
                topic_data[topic_name].append((time_sec, msg.throttle, msg.brake, msg.steer))
            elif topic_name == '/carla/ego_vehicle/waypoints':
                msg = deserialize_message(serialized_msg, Path)
                if len(msg.poses) > 0:
                    first_pose = msg.poses[0].pose
                    topic_data[topic_name].append((time_sec, first_pose.position.x, first_pose.position.y, first_pose.position.z,
                                                   first_pose.orientation.x,  # Yaw
                                                   first_pose.orientation.w))  # Reference velocity
            elif topic_name == '/norm_error':  # Read norm error values
                msg = deserialize_message(serialized_msg, Float32)
                topic_data[topic_name].append((time_sec, msg.data))  # Store norm_error values

    return topic_data

def calculate_rmse(ref_x, ref_y, actual_x, actual_y):
    """ Compute RMSE (Root Mean Square Error) for trajectory tracking """
    ref_x, ref_y = np.array(ref_x), np.array(ref_y)
    actual_x, actual_y = np.array(actual_x), np.array(actual_y)

    min_length = min(len(ref_x), len(actual_x))  # Ensure matching size
    ref_x, ref_y = ref_x[:min_length], ref_y[:min_length]
    actual_x, actual_y = actual_x[:min_length], actual_y[:min_length]

    errors = np.sqrt((actual_x - ref_x) ** 2 + (actual_y - ref_y) ** 2)
    rmse = np.sqrt(np.mean(errors ** 2))

    print(f"🚀 Trajectory Tracking RMSE: {rmse:.4f} meters")
    return rmse

def compute_norm_error_rmse(topic_data):
    """ Compute RMSE for norm error """
    if '/norm_error' in topic_data and len(topic_data['/norm_error']) > 0:
        _, norm_errors = zip(*topic_data['/norm_error'])  # Extract norm error values
        norm_errors = np.array(norm_errors)

        rmse = np.sqrt(np.mean(norm_errors ** 2))  # Compute RMSE
        print(f"🔥 Norm Error RMSE: {rmse:.4f} meters")
        return rmse
    else:
        print("⚠️ No norm error data found in the ROS bag.")
        return None

def plot_vehicle_data(topic_data):
    if '/carla/ego_vehicle/odometry' in topic_data and '/carla/ego_vehicle/waypoints' in topic_data:
        odom_times, odom_x, odom_y, odom_z, odom_yaw, odom_long_vel = zip(*topic_data['/carla/ego_vehicle/odometry'])
        traj_times, traj_x, traj_y, traj_z, traj_yaw, traj_ref_vel = zip(*topic_data['/carla/ego_vehicle/waypoints'])

        # Plot X Position

        plt.figure()
        plt.plot(odom_x, odom_y, label='Vehicle position')
        plt.plot(traj_x, traj_y, label='Reference Waypoints', linestyle='--')
        plt.legend()
        plt.xlabel('X Position in m')
        plt.ylabel('Y Position in m')
        plt.title('Vehicle Position vs Reference Waypoints')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))  # Fix time axis
        

        plt.figure()
        plt.plot(odom_times, odom_x, label='Vehicle X')
        plt.plot(traj_times, traj_x, label='Waypoints X', linestyle='--')
        plt.legend()
        plt.xlabel('Time in seconds')
        plt.ylabel('X Position in m')
        plt.title('Vehicle Position X vs Waypoints')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))  # Fix time axis
        
        # Plot Y Position
        plt.figure()
        plt.plot(odom_times, odom_y, label='Vehicle Y')
        plt.plot(traj_times, traj_y, label='Waypoints Y', linestyle='--')
        plt.legend()
        plt.xlabel('Time in seconds')
        plt.ylabel('Y Position in m')
        plt.title('Vehicle Position Y vs Waypoints')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        # Plot Yaw Angle
        plt.figure()
        plt.plot(odom_times, np.rad2deg(odom_yaw), label='Vehicle Yaw Angle')
        plt.plot(traj_times, np.rad2deg(traj_yaw), label='Reference Yaw', linestyle='--')

        #print(traj_yaw)
        len_min = min(len(traj_yaw), len(odom_yaw))
        diff = np.rad2deg(np.arccos(np.cos(np.array(traj_yaw[0:len_min]) - np.array(odom_yaw[0:len_min]))) ) 
        #diff = np.rad2deg(np.array(traj_yaw[0:len_min] - np.array(odom_yaw[0:len_min])) )
        
        plt.plot(odom_times[0:len_min], diff, label='Difference in Angles', color='r')
        
        plt.legend()
        plt.xlabel('Time in seconds')
        plt.ylabel('Yaw Angle in degree')
        plt.title('Vehicle Heading Angle vs Reference Yaw')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        # Plot Longitudinal Velocity
        plt.figure()
        plt.plot(odom_times, odom_long_vel, label='Longitudinal Velocity')
        plt.plot(traj_times, traj_ref_vel, label='Reference Velocity', linestyle='--')
        plt.legend()
        
        plt.xlabel('Time in seconds')
        plt.ylabel('Velocity in m/s')
        plt.ylim(-5,20 )
        plt.title('Longitudinal Velocity vs Reference Velocity')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    if '/carla/ego_vehicle/vehicle_control_cmd' in topic_data:
        times, throttle, brake, steer = zip(*topic_data['/carla/ego_vehicle/vehicle_control_cmd'])
        steer_in_deg = np.rad2deg(steer)
        plt.figure()
        plt.plot(times, throttle, label='Throttle')
        plt.xlabel('Time in seconds')
        plt.ylabel('Throttle (0 to 1)')
        plt.title('Throttle Command')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        plt.figure()
        plt.plot(times, brake, label='Brake')
        plt.xlabel('Time in seconds')
        plt.ylabel('Brake (0 to 1)')
        plt.title('Brake Command')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        plt.figure()
        plt.plot(times, steer_in_deg, label='Steer')
        plt.xlabel('Time in seconds')
        plt.ylabel('Steering Angle in degree')
        plt.title('Steering Command')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    if 'global_path' in topic_data:
        time, x, y = zip(*topic_data['global_path'])
        #print(x[0], y[0])
        plt.figure()
        plt.plot(x[0],y[0])
        plt.xlabel("X in m")
        plt.ylabel("Y in m")
        plt.grid(True)
        plt.title("Path Generated by Planner")
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    plt.legend()
    plt.show()

# Read and process data
bag_path = "/home/swati/Motion_Planning/MP_for_AV/multi_topic_bag"
data = read_vehicle_bag_data(bag_path)

# Compute RMSE for norm error
compute_norm_error_rmse(data)

# Plot data
plot_vehicle_data(data)

