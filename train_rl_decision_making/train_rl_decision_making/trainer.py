import carla
from env import  Env
from network import ActorCritic
from agent_PPO import AgentPPO
from buffer import RolloutBuffer
import rclpy
from waypoint_node import WaypointPublisher
import torch


class Trainer:
    def __init__(self,env, network, agent, buffer, max_env_step_counts):
        self.env = env
        self.network = network
        self.agent = agent
        self.buffer = buffer
        self.max_env_step_counts = max_env_step_counts

    def collect_rollout(self, state):
        done = False
        while self.buffer.ptr < self.buffer.buffer_size:
            action, log_prob, value = self.agent.get_action(state)

            action_env = action.squeeze(0).detach().cpu().numpy()
            next_state, reward, done, info = self.env.step(action_env)

            self.buffer.store(state, action, reward, done, log_prob, value)

            if done:
                state = self.env.reset()
            else:
                state = next_state

        return state, self.buffer.ptr

    def train_network(self):
        steps = 0
        state = self.env.reset()

        while steps < self.max_env_step_counts:
            state, rollout_steps_collected = self.collect_rollout(state)

            with torch.no_grad():
                _, _, last_value = self.agent.get_action(state)

            gamma = self.agent.gamma
            gae_lambda = self.agent.gae_lambda

            self.buffer.compute_advantages(last_value, gamma=gamma, gae_lambda=gae_lambda)
            self.agent.update()
            self.buffer.clear()
            steps += rollout_steps_collected

    def evaluate(self, state):
        action, log_prob, value = self.agent.get_action(state)
        return action, log_prob, value


if __name__ == "__main__":
        buffer_size = 2048
        state_dim_1 = 21 
        state_dim = 9 
        act_dim = 30
        device = torch.device()
        rclpy.init()
        waypoint_publisher = WaypointPublisher()
        env = Env(1, waypoint_publisher, traffic_manager_port=8000, traffic_size=5, v_min=0.0, v_max=10.0,
                   a_min=-3.0, a_max=3.0, lateral_accel=2.0, max_obj=10,N = 10, tf=5, traj_resolution =0.25, 
                   goal_radius=2, lidar_max_range=50)
        model = ActorCritic(columns=9, obs_size=10, traj_size=10, action_dim=10)
        PPO = AgentPPO()
        buffer = RolloutBuffer(buffer_size, (state_dim_1, state_dim), act_dim, device="cpu")

