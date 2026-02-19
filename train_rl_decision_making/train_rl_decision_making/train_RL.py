from waypoint_node import WaypointPublisher
from env import Env 
import rclpy
import numpy as np
from network import ActorCritic
import torch 

if __name__ == "__main__":
   rclpy.init()
   waypoint_publisher = WaypointPublisher()
   env = Env(1, waypoint_publisher, traffic_manager_port=8000, traffic_size=5, v_min=0.0, v_max=10.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0, max_obj=10,N = 10, tf=5, traj_resolution =0.25, goal_radius=2, lidar_max_range=50)
   model = ActorCritic(in_dim=9, obs_size=10, traj_size=10, action_dim=30)
   #state normalizer 
   
   
   for _ in range(10):
        
        try:
            env.reset()
        except:
            print("Reset failed, retrying...")
            continue  # skip to the next iteration if reset fails

        print("Environment reset successful")

        for _ in range(3): 
            print("Step in environment")   
            x = torch.randn(1, 21, 9)
            action, logprob, value = model(x)  # Add batch dimension
            print("Action from model:", action.shape)
            
            action = action.detach().numpy().squeeze(0)  # Remove batch dimension
            action = action.reshape(-1, 3)  # Reshape to (10, 3)
            state  = env.step(action)  # Remove batch dimension
            ego_location =   env.get_ego_location()
            print("Ego location:", ego_location)

   env.destroy()  # Clean up CARLA actors and sensors
   
   rclpy.spin_once(waypoint_publisher)
   
   waypoint_publisher.destroy_node()
   rclpy.shutdown()