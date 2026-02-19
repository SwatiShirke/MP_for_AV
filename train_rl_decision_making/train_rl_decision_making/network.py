import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal


class ActorCritic(nn.Module):
    def __init__(self, in_dim, obs_size, traj_size, action_dim,
                 hidden_size=128, fused_size=256, init_log_std=-0.5, action_scale=1.0):
        super().__init__()

        self.obs_size = obs_size
        self.traj_size = traj_size
        self.action_scale = action_scale

        self.MLP1 = nn.Sequential(
            nn.Linear(in_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )

        cat_size = 5 * hidden_size  # ego + (max,mean obs) + (max,mean traj)

        self.MLP2 = nn.Sequential(
            nn.Linear(cat_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, fused_size),
            nn.ReLU()
        )

        self.actor_head = nn.Sequential(
            nn.Linear(fused_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, action_dim)
        )

        self.critic_head = nn.Sequential(
            nn.Linear(fused_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, 1)
        )

        self.log_std = nn.Parameter(torch.ones(action_dim) * init_log_std)

    def _dist_and_value(self, x):
        ego_info = self.MLP1(x[:, 0, :])

        obs_tokens = x[:, 1:self.obs_size + 1, :]
        obs_info = self.MLP1(obs_tokens)
        max_obs = obs_info.max(dim=1).values
        mean_obs = obs_info.mean(dim=1)

        traj_tokens = x[:, self.obs_size + 1:self.obs_size + 1 + self.traj_size, :]
        traj_info = self.MLP1(traj_tokens)
        max_traj = traj_info.max(dim=1).values
        mean_traj = traj_info.mean(dim=1)

        cat_tensor = torch.cat([ego_info, max_obs, mean_obs, max_traj, mean_traj], dim=-1)
        fused_info = self.MLP2(cat_tensor)

        mean = self.actor_head(fused_info) * self.action_scale
        log_std = self.log_std.unsqueeze(0).expand_as(mean)
        log_std = torch.clamp(log_std, -20.0, 2.0)

        value = self.critic_head(fused_info)
        return mean, log_std, value

    def forward(self, x):
        mean, log_std, value = self._dist_and_value(x)
        std = torch.exp(log_std)
        dist = Normal(mean, std)
        action = dist.rsample()
        logprob = dist.log_prob(action).sum(dim=-1)
        return action, logprob, value

    def evaluate(self, states, actions):
        mean, log_std, value = self._dist_and_value(states)
        std = torch.exp(log_std)
        dist = Normal(mean, std)
        logp = dist.log_prob(actions).sum(dim=-1)
        entropy = dist.entropy().sum(dim=-1)
        return logp, entropy, value



if __name__ == "__main__":
    B = 64
    x = torch.randn(B, 21, 9)

    model = ActorCritic(in_dim=9, obs_size=10, traj_size=10, action_dim=10)
    action, logprob, value = model(x)

    print("action", action.shape, "logprob", logprob.shape, "value", value.shape)

        


        












        
