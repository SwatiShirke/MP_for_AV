import argparse
import torch
import numpy as np
from network import ActorCritic
from ppo import compute_gae, ppo_update
from carla_env import CarlaEnv

def collect_trajectory(env, ac_model, device, max_steps=2048):
    obs_buf = []
    actions_buf = []
    logp_buf = []
    rewards_buf = []
    masks_buf = []
    values_buf = []
    obs = env.reset()
    for _ in range(max_steps):
        obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(device)
        with torch.no_grad():
            action, logp, _ = ac_model.act(obs_t)
            value = ac_model.critic(obs_t)
        action_item = action.cpu().numpy()[0]
        next_obs, reward, done, _ = env.step(int(action_item))
        obs_buf.append(obs)
        actions_buf.append(action_item)
        logp_buf.append(logp.cpu().numpy())
        rewards_buf.append(reward)
        masks_buf.append(0.0 if done else 1.0)
        values_buf.append(value.cpu().numpy()[0])
        obs = next_obs
        if done:
            obs = env.reset()
            break
    obs_arr = torch.tensor(np.array(obs_buf), dtype=torch.float32).to(device)
    actions_arr = torch.tensor(np.array(actions_buf), dtype=torch.long).to(device)
    old_logp_arr = torch.tensor(np.array(logp_buf), dtype=torch.float32).squeeze().to(device)
    rewards_t = torch.tensor(np.array(rewards_buf), dtype=torch.float32).to(device)
    masks_t = torch.tensor(np.array(masks_buf), dtype=torch.float32).to(device)
    values = torch.tensor(np.concatenate([np.array(values_buf), np.array([0.0])]), dtype=torch.float32).to(device)
    returns, advantages = compute_gae(rewards_t, masks_t, values)
    return obs_arr, actions_arr, old_logp_arr, returns.detach(), advantages.detach()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--device', default='cpu')
    args = parser.parse_args()
    device = torch.device(args.device)
    env = CarlaEnv()
    obs_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    ac = ActorCritic(obs_dim, action_dim).to(device)
    optimizer = torch.optim.Adam(ac.parameters(), lr=3e-4)
    for ep in range(args.episodes):
        obs, actions, old_logp, returns, advantages = collect_trajectory(env, ac, device)
        ppo_update(ac, optimizer, obs, actions, old_logp, returns, advantages)
        if ep % 10 == 0:
            print(f"Episode {ep} completed")

if __name__ == '__main__':
    main()
