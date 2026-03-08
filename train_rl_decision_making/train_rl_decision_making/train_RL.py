from waypoint_node import WaypointPublisher
from env import Env 
import rclpy
import numpy as np
from network import ActorCritic
import torch 
from odom_node import OdomPublisher

if __name__ == "__main__":
   rclpy.init()
   waypoint_publisher = WaypointPublisher()
   odom_publisher = OdomPublisher()
   
   env = Env(0.25,1.00 ,odom_publisher, waypoint_publisher, traffic_manager_port=8000, traffic_size=20,
                   v_min=0.0, v_max=5.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0, max_obj=10,N = 10, 
                   tf=5, traj_resolution =0.25, goal_radius=2, lidar_max_range=50, delta_x_th=0.5, delta_y_th=0.1,
                   delta_yaw_th=0.5, is_test_mode=  True)
   
   #state normalizer 
   
   for _ in range(1):
        #env.reset()
        #try:
        state, traj  = env.reset()
        print("traj shape: ", traj.shape)
        print("traj waypoints: ", traj[:,0:3])
        # except:
        #     print("Reset failed, retrying...")
        #     continue  # skip to the next iteration if reset fails

        print("Environment reset successful")

        for i in range(500):                 
            
            state, reward, done, info,traj   = env.step(traj[:, 0:3])  # Remove batch dimension
        
        if env.is_test_mode:
                    video_path = f"episode_{i}.mp4"
                    #if env.episode_idx % 100 == 0:  # save every 10 episodes
                    try:
                        env.save_top_view_video(video_path, fps=20.0, clear_buffer=True)
                    except ValueError:
                        # no frames captured or buffer missing
                        pass

   env.destroy()  # Clean up CARLA actors and sensors
   
   rclpy.spin_once(waypoint_publisher)
   
   waypoint_publisher.destroy_node()
   odom_publisher.destroy_node()
   rclpy.shutdown()