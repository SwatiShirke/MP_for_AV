import os
import rosbag2_py
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # Import ticker for formatting
from rclpy.serialization import deserialize_message
from nav_msgs.msg import Odometry, Path
from carla_msgs.msg import CarlaEgoVehicleControl
from std_msgs.msg import Float32  # Import Float32 for norm_error topic
import numpy as np
from vd_msgs.msg import VDPath, VDpose, VDtraj
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import io
from PIL import Image


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
        '/norm_error',  # Include norm_error topic
        'explored_nodes',
        'predicted_path',
        '/vehicle_est_pose'
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
                print("got odom data")
                msg = deserialize_message(serialized_msg, VDpose)
                topic_data[topic_name].append((time_sec, msg.x, msg.y, msg.psi,
                                               msg.velocity,  # Yaw angle
                                               msg.distance))  # Longitudinal velocity
            if topic_name == "/vehicle_est_pose":
                print("got est data")
                msg = deserialize_message(serialized_msg, VDpose)
                topic_data[topic_name].append((time_sec, msg.x, msg.y, msg.psi,
                                               msg.velocity,  # Yaw angle
                                               msg.distance))  # Longitudinal velocity   

            if topic_name == '/carla/ego_vehicle/vehicle_control_cmd':
                msg = deserialize_message(serialized_msg, CarlaEgoVehicleControl)
                topic_data[topic_name].append((time_sec, msg.throttle, msg.brake, msg.steer))
            if topic_name == '/carla/ego_vehicle/waypoints':
                msg = deserialize_message(serialized_msg, VDtraj)
                if len(msg.poses) > 0:
                    first_pose = msg.poses[0]
                    topic_data[topic_name].append((time_sec, first_pose.x, first_pose.y, first_pose.psi,
                                                   first_pose.velocity,  # Yaw
                                                   first_pose.distance))  # Reference velocity
                    
            if topic_name == 'predicted_path':
                msg = deserialize_message(serialized_msg, VDtraj)
                if len(msg.poses) > 0:
                    first_pose = msg.poses[1]
                    topic_data[topic_name].append((time_sec, first_pose.x, first_pose.y, first_pose.psi,
                                                   first_pose.velocity,  # Yaw
                                                   first_pose.distance))  # Reference velocity
            
            if topic_name == '/norm_error':  # Read norm error values
                msg = deserialize_message(serialized_msg, Float32)
                topic_data[topic_name].append((time_sec, msg.data))  # Store norm_error values
            
            if topic_name == 'explored_nodes':                
                msg = deserialize_message(serialized_msg, VDPath)                
                topic_data[topic_name].append((time_sec, msg.x_val, msg.y_val))
          

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
    if  topic_data['/carla/ego_vehicle/odometry'] != [] and topic_data['/carla/ego_vehicle/waypoints'] != [] and topic_data['predicted_path'] != []:
        odom_times, odom_x, odom_y, odom_yaw, odom_long_vel, odom_distance = zip(*topic_data['/carla/ego_vehicle/odometry'])
        est_times, est_x, est_y, est_yaw, est_long_vel, est_distance = zip(*topic_data['/vehicle_est_pose'])
        traj_times, traj_x, traj_y, traj_yaw, traj_ref_vel, ref_distance = zip(*topic_data['/carla/ego_vehicle/waypoints'])
        mpc_pred_times, mpc_pred_x, mpc_pred_y, mpc_pred_yaw, mpc_pred_ref_vel, mpc_pred_distance = zip(*topic_data['predicted_path'])

        # Plot X Position
        plt.figure()
        plt.plot(odom_x, odom_y, label='Ground truth pose', linestyle='-')
        plt.plot(traj_x, traj_y, label='Hybrid A* Path', linestyle='--')
        plt.plot(est_x, est_y, label='Estimated Pose', linestyle='-.')
        #plt.plot(mpc_pred_x, mpc_pred_y, label='MPC Predicted Path', linestyle='-.')
        plt.legend()
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Vehicle Position vs Reference Waypoints')
        plt.grid(True)
        #plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))  # Fix time axis

        plt.figure()
        plt.plot(odom_times, odom_x, label='Vehicle X')
        plt.plot(traj_times, traj_x, label='Waypoints X', linestyle='--')
        plt.plot(mpc_pred_times, mpc_pred_x, label='MPC Predicted Path X', linestyle='-.')
        plt.legend()
        plt.xlabel('Time (seconds)')
        plt.ylabel('X Position')
        plt.title('Vehicle X Position vs Waypoints') 
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))  # Fix time axis
        
        # Plot Y Position
        plt.figure()
        plt.plot(odom_times, odom_y, label='Vehicle Y')
        plt.plot(traj_times, traj_y, label='Waypoints Y', linestyle='--')
        plt.plot(mpc_pred_times, mpc_pred_y, label='MPC Predicted Path Y', linestyle='-.')
        plt.legend()
        plt.xlabel('Time (seconds)')
        plt.ylabel('Y Position')
        plt.title('Vehicle Y Position vs Waypoints')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        # Plot Yaw Angle
        plt.figure()
        plt.plot(odom_times, odom_yaw, label='Yaw Angle')
        plt.plot(traj_times, traj_yaw, label='Reference Yaw', linestyle='--')
        plt.plot(mpc_pred_times, traj_yaw, label='Reference Yaw', linestyle='--')
        plt.legend()
        plt.xlabel('Time (seconds)')
        plt.ylabel('Yaw Angle')
        plt.title('Yaw Angle vs Reference Yaw')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        # Plot Longitudinal Velocity
        plt.figure()
        plt.plot(odom_times, odom_long_vel, label='Longitudinal Velocity')
        plt.plot(traj_times, traj_ref_vel, label='Reference Velocity', linestyle='--')
        plt.legend()
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity')
        plt.ylim(0, 45)
        plt.title('Longitudinal Velocity vs Reference Velocity')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    if topic_data['/carla/ego_vehicle/vehicle_control_cmd'] != []:
        times, throttle, brake, steer = zip(*topic_data['/carla/ego_vehicle/vehicle_control_cmd'])
        
        plt.figure()
        plt.plot(times, throttle, label='Throttle')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Throttle')
        plt.title('Throttle Command Over Time')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        plt.figure()
        plt.plot(times, brake, label='Brake')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Brake')
        plt.title('Brake Command Over Time')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

        plt.figure()
        plt.plot(times, steer, label='Steer')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Steering Angle')
        plt.title('Steering Command Over Time')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    if topic_data['global_path'] != []:
        time, x, y = zip(*topic_data['global_path'])
        #print(x[0], y[0])
        plt.figure()
        plt.plot(x[0],y[0])
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.title("path")
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    # if topic_data['explored_nodes'] != []: 
    #     grid_resolution = 0.25      
    #     time, x, y = zip(*topic_data['explored_nodes'])         
    #     x,y = np.array(x[0]), np.array(y[0]) 
    #     print(len(x), len(y))    
    #     path = np.hstack((x.reshape(-1,1),y.reshape(-1, 1)))
    #     frames = [] 

    #     # Create frames
    #     for i in range(len(x)):
    #         fig, ax = plt.subplots(figsize=(5, 5))
    
    #         # Set axis limits based on the min/max of x and y
    #         # ax.set_xlim(np.min(x), np.max(x))
    #         # ax.set_ylim(np.min(y), np.max(y))

    #         ax.set_xlim(np.min(x)-grid_resolution, np.max(x)+grid_resolution)
    #         ax.set_ylim(np.min(y)-grid_resolution, np.max(y)+grid_resolution)
            
    #         # Plot the explored nodes up to the current frame (green dots)
    #         ax.plot(x[:i+1], y[:i+1], 'go', markersize=6)  
    
    #         # Remove axis labels and ticks for a cleaner plot
    #         ax.set_xticks(np.linspace(np.min(x), np.max(x), 10))
    #         ax.set_yticks(np.linspace(np.min(y), np.max(y), 10))
            
            
    #         # Save the frame to memory
    #         buf = io.BytesIO()
    #         plt.savefig(buf, format='png')
    #         buf.seek(0)
    #         frames.append(Image.open(buf))
    #         plt.close()
    
    #     # Save the frames as a GIF
    #     frames[0].save('explored_nodes_points.gif', save_all=True, append_images=frames[1:], duration=300, loop=0, format='GIF')

    #     print("GIF saved successfully!")

        


    plt.legend()
    plt.show()

# Read and process data
bag_path = "/home/swati/Motion_Planning/MP_for_AV/multi_topic_bag"
data = read_vehicle_bag_data(bag_path)

# Compute RMSE for norm error
compute_norm_error_rmse(data)

# Plot data
plot_vehicle_data(data)

