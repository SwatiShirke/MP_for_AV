import torch
import torch.nn as nn
from torch.distributions import Normal


class ActorCritic(nn.Module):
    def __init__(
        self,
        in_dim: int,
        obs_size: int,
        traj_size: int,
        action_dim: int,
        hidden_size: int = 128,
        fused_size: int = 256,
        init_log_std: float = -0.5,
        delta_x_max: float = 2.0,
        delta_y_max: float = 1.0,
        delta_yaw_max: float = 0.4,
    ):
        super().__init__()

        self.obs_size = obs_size
        self.traj_size = traj_size

        # -------- action scale (must match action_dim) --------
        # If your action is 10 waypoints × 3 = 30, action_dim must be 30.
        if action_dim % 3 != 0:
            raise ValueError(
                f"action_dim={action_dim} must be multiple of 3 for (dx,dy,dyaw) packing."
            )
        n_wp = action_dim // 3
        scale = torch.tensor([delta_x_max, delta_y_max, delta_yaw_max] * n_wp, dtype=torch.float32)
        self.register_buffer("action_scale", scale)  # (action_dim,)

        # -------- shared token encoder --------
        self.MLP1 = nn.Sequential(
            nn.Linear(in_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )

        cat_size = 5 * hidden_size  # ego + (max,mean obs) + (max,mean traj)

        self.MLP2 = nn.Sequential(
            nn.Linear(cat_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, fused_size),
            nn.ReLU(),
        )

        self.actor_head = nn.Sequential(
            nn.Linear(fused_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, action_dim),
        )

        self.critic_head = nn.Sequential(
            nn.Linear(fused_size, fused_size),
            nn.ReLU(),
            nn.Linear(fused_size, 1),
        )

        self.log_std = nn.Parameter(torch.ones(action_dim) * init_log_std)

    def _dist_and_value(self, x: torch.Tensor):
        ego_info = self.MLP1(x[:, 0, :])

        obs_tokens = x[:, 1 : self.obs_size + 1, :]
        obs_info = self.MLP1(obs_tokens)
        max_obs = obs_info.max(dim=1).values
        mean_obs = obs_info.mean(dim=1)

        traj_tokens = x[:, self.obs_size + 1 : self.obs_size + 1 + self.traj_size, :]
        traj_info = self.MLP1(traj_tokens)
        max_traj = traj_info.max(dim=1).values
        mean_traj = traj_info.mean(dim=1)

        cat_tensor = torch.cat([ego_info, max_obs, mean_obs, max_traj, mean_traj], dim=-1)
        fused_info = self.MLP2(cat_tensor)

        mean = self.actor_head(fused_info)  # unscaled
        log_std = self.log_std.unsqueeze(0).expand_as(mean)
        log_std = torch.clamp(log_std, -5.0, 1.0)
        value = self.critic_head(fused_info)

        return mean, log_std, value

    def forward(self, x: torch.Tensor):
        mean, log_std, value = self._dist_and_value(x)
        std = torch.exp(log_std)
        dist = Normal(mean, std)

        # tanh-squashed + scaled actions
        z = dist.rsample()            # pre-squash
        a = torch.tanh(z)             # (-1,1)
        action = a * self.action_scale  # per-dim bounds

        # correct log-prob for tanh squash
        logprob = dist.log_prob(z).sum(dim=-1)
        logprob -= torch.sum(torch.log(1.0 - a.pow(2) + 1e-6), dim=-1)
        logprob = logprob.unsqueeze(-1)

        return action, logprob, value

    def evaluate(self, states: torch.Tensor, actions: torch.Tensor):
        mean, log_std, value = self._dist_and_value(states)
        std = torch.exp(log_std)
        dist = Normal(mean, std)

        # invert scaling + tanh to recover z for correct log_prob
        a = actions / (self.action_scale + 1e-8)
        a = torch.clamp(a, -1.0 + 1e-6, 1.0 - 1e-6)
        z = 0.5 * (torch.log1p(a) - torch.log1p(-a))  # atanh(a)

        logp = dist.log_prob(z).sum(dim=-1)
        logp -= torch.sum(torch.log(1.0 - a.pow(2) + 1e-6), dim=-1)
        logp = logp.unsqueeze(-1)

        entropy = dist.entropy().sum(dim=-1, keepdim=True)  # (B,1)
        return logp, entropy, value


if __name__ == "__main__":
    B = 64
    x = torch.randn(B, 21, 9)

    # 10 waypoints × (dx,dy,dyaw) = 30
    model = ActorCritic(
        in_dim=9, obs_size=10, traj_size=10, action_dim=30,
        hidden_size=128, fused_size=256, init_log_std=-0.5,
        delta_x_max=2.0, delta_y_max=1.0, delta_yaw_max=0.4
    )

    action, logprob, value = model(x)
    print("action", action.shape, "logprob", logprob.shape, "value", value.shape)