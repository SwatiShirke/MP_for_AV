import os

import carla
from utilities import Utilities
from env import  Env
from network import ActorCritic
from agent_PPO import AgentPPO
from buffer import RolloutBuffer
import rclpy
from waypoint_node import WaypointPublisher
from odom_node import OdomPublisher
from utilities import Utilities
import torch
import wandb
import os, subprocess
import math

class Trainer:
    def __init__(self,env, agent, buffer, max_env_step_counts, utilties_obj, no_epoch, clip_eps, max_grad_norm, 
                 minibatch_size, gamma, gae_lambda, buffer_size, lr):
        self.env = env        
        self.agent = agent        
        self.buffer = buffer
        self.max_env_step_counts = max_env_step_counts
        self.utilities = utilties_obj
        self.no_epoch = no_epoch
        self.clip_eps = clip_eps        
        self.max_grad_norm = max_grad_norm
        self.minibatch_size = minibatch_size
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.rollout_size = buffer_size
        self.lr = lr
        ##W&B logging variables       
        self.env_steps = 0
        self.update_idx = 0
        self.episode_idx = 0
        self.ep_return = 0.0
        self.ep_len = 0
        self.is_test_mode = env.is_test_mode
        
        wandb.init(
            project="ppo-autonomous-driving",   # change to your project name
            name="ppo_run_1",                   # optional run name
            config={
                "algo": "PPO",
                "gamma": self.gamma,
                "gae_lambda": self.gae_lambda,
                "clip_eps": self.clip_eps,
                "rollout_steps": self.rollout_size,
                "update_epochs": self.no_epoch,
                "minibatch_size": self.minibatch_size,
                "lr": self.lr
            }
        )

    def fd_count(self):
        return len(os.listdir("/proc/self/fd"))
    
    def fd_breakdown(self, pid=None):
        pid = pid or os.getpid()
        # show top FD "targets"
        out = subprocess.check_output(
            ["bash", "-lc", f"lsof -p {pid} | awk '{{print $9}}' | sed 's#/.*##' | sort | uniq -c | sort -nr | head"]
        ).decode()
        return out

    def collect_rollout(self, in_state):
        done = False
        while self.buffer.ptr < self.buffer.buffer_size:
            # self_fd_count = self.fd_count()
            # print(f"Step {self.env_steps}, FD count: {self_fd_count}")
            # print(self.fd_breakdown())

            #print("state before preprocess", in_state)
            state = self.utilities.preprocess_state(in_state)
            #print("Input state ", state)
            
            #print("state size after preprocess", state.shape)
            state = state.unsqueeze(0)
            #print("state size before network", state.shape)
            action, log_prob, value = self.agent.get_action(state)
            # print("state size after get_action", state.shape)
            # print("action size after get_action", action.shape) 
            # print("log_prob size after get_action", log_prob.shape)
            # print("value size after get_action", value.shape)
            state = state.squeeze(0)
            action = action.squeeze(0)
            log_prob = log_prob.squeeze(0)
            value = value.squeeze(0)
            # print("state size after get_action", state.shape)
            # print("action size after get_action", action.shape) 
            # print("log_prob size after get_action", log_prob.shape)
            # print("value size after get_action", value.shape)
            
            # print("state type", type(state))
            # print("action type", type(action))
            # print("log_prob type", type(log_prob))
            # print("value type", type(value))

            action_env = action.detach().cpu().numpy() 
            # print("ego state ", self.env.get_ego_state()) 
            # print("action_env ", action_env) 
            # print("action_env", action_env)         
            ego_state = self.env.get_ego_state()
            # print("action_env ", action_env)
            # print("ego_state ", ego_state)
            ref_traj_ego = self.env.traj_waypoints_ego  
            #print("ref_traj_ego ", ref_traj_ego)  
            action_processed = self.utilities.postprocess_2(action_env, ego_state, ref_traj_ego)
            #print("action_processed ", action_processed)
            next_state, reward, done, info = self.env.step(action_processed)
            # reward = torch.tensor(reward, dtype=torch.float32)
            # done = torch.tensor(done, dtype=torch.float32)

           
            self.env_steps += 1
            self.ep_return += float(reward)
            self.ep_len += 1

            self.buffer.store(state, action, reward, done, log_prob, value)

            if done:                
                print("Reward for episode: ", self.ep_return )  
                print("reason for episode termination: ", info)           
                self.episode_idx += 1
                wandb.log({
                        "episode/return": self.ep_return,
                        "episode/length": self.ep_len,
                        # "episode/index": self.episode_idx,
                        })
                
                self.ep_return = 0.0
                self.ep_len = 0 

                #save caemra frames as videos
                if self.is_test_mode:
                    video_path = f"episode_{self.episode_idx:05d}.mp4"
                    #if self.episode_idx % 100 == 0:  # save every 10 episodes
                    try:
                        env.save_top_view_video(video_path, fps=20.0, clear_buffer=True)
                    except ValueError:
                        # no frames captured or buffer missing
                        pass
                
                in_state = self.env.reset() 
                #break  # end rollout collection on episode end

                while in_state is None:
                    print("Reset failed, retrying...")
                    in_state = self.env.reset()
            else:
                in_state = next_state
           
        #print("state after step", state.shape)
        return in_state, self.buffer.ptr

    def train_network(self):
        steps = 0
        state = self.env.reset()
        while state is None:
                    print("Reset failed, retrying...")
                    state = self.env.reset()

        while steps < self.max_env_step_counts:
            
            state, rollout_steps_collected = self.collect_rollout(state)            
            #break #for debug - remove this break to enable training loop
            #print("rollout step returned", state.shape)
            last_state = self.utilities.preprocess_state(state)           
            #print("state size after preprocess", last_state.shape)
            last_state = last_state.unsqueeze(0)
            
            with torch.no_grad():
                _, _, last_value = self.agent.get_action(last_state)

            gamma = self.agent.gamma
            gae_lambda = self.agent.gae_lambda

            self.buffer.compute_advantages(last_value, gamma=gamma, gae_lambda=gae_lambda)
            policy_loss, value_loss, total_loss, entropy = self.agent.update()

            self.buffer.clear()            
            self.update_idx += 1 

            if self.update_idx % 10 == 0:
                self.save_model("ppo_checkpoint.pth")

            wandb.log({
                "loss/policy": policy_loss,
                "loss/value": value_loss,
                "loss/total": total_loss,
                "stats/entropy": entropy,
                # "stats/approx_kl": approx_kl,
                # "stats/clip_fraction": clip_frac,
                #"update/index": self.update_idx
            })          

            steps += rollout_steps_collected

    def evaluate(self, state):
        action, log_prob, value = self.agent.get_action(state)
        return action, log_prob, value

    def save_model(self, path):
        self.agent.save_model(path, self.env_steps, self.episode_idx)


if __name__ == "__main__":
        buffer_size = 2048
        state_dim_1 = 21 
        state_dim_2 = 9 
        act_dim = 30
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        no_of_epochs = 10
        clip_eps = 0.2
        max_grad_norm = 0.5
        minibatch_size = 64
        gamma = 0.99
        gae_lambda = 0.95 
        max_env_step_count = 5000000  
        vf_coeff=0.5
        ent_coeff=0.01
        lr=1e-4
        delta_x_max = 10.0
        delta_y_max = 10.0
        delta_yaw_max = math.pi / 2
        grid_resolution = 0.5
        min_distance_lidar = 0.5
        checkpoint_path = "ppo_checkpoint.pth"
        rclpy.init() 
        waypoint_publisher = WaypointPublisher()
        odom_publisher = OdomPublisher()

        env = Env(grid_resolution, min_distance_lidar, odom_publisher, waypoint_publisher, traffic_manager_port=8000, traffic_size=15,
                   v_min=0.0, v_max=5.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0, max_obj=10,N = 10, 
                   tf=5, traj_resolution =0.25, goal_radius=2, lidar_max_range=50, delta_x_th=0.5, delta_y_th=0.1,
                   delta_yaw_th=0.5, is_test_mode=  False, max_episode_steps=500) 


        model = ActorCritic(in_dim=9, obs_size=10, traj_size=10, action_dim=act_dim, delta_x_max=delta_x_max, delta_y_max=delta_y_max, delta_yaw_max=delta_yaw_max)
        buffer = RolloutBuffer(buffer_size, (state_dim_1, state_dim_2), act_dim, device="cpu")
        optimizer = torch.optim.Adam(model.parameters(), lr)
        total_updates = int(max_env_step_count / buffer_size)
        scheduler = torch.optim.lr_scheduler.LinearLR(
                        optimizer,
                        start_factor=1.0,
                        end_factor=0.1,
                        total_iters=total_updates
                        )
        PPO = AgentPPO(model, optimizer, scheduler, buffer,no_of_epochs, clip_eps, vf_coeff, ent_coeff, max_grad_norm, minibatch_size, gamma, gae_lambda, chkpoint_path=checkpoint_path)
        utilities = Utilities(max_L=12, max_W=5, lidar_max_range=50, v_max=10, tf=5)
        trainer = Trainer(env, PPO, buffer, max_env_step_count, utilities, no_of_epochs, clip_eps, max_grad_norm, minibatch_size, gamma, gae_lambda, buffer_size, lr)
        trainer.train_network()



