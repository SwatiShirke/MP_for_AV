import torch
import numpy as np

class RolloutBuffer:
    def __init__(self, buffer_size, state_shape, act_dim, device="cpu"):
        self.buffer_size = buffer_size
        self.device = torch.device(device)

        # Storage tensors
        self.states = torch.zeros((buffer_size, *state_shape), device=self.device)  # (T, 21, 9)
        self.actions = torch.zeros((buffer_size, act_dim), device=self.device)
        self.rewards = torch.zeros(buffer_size, device=self.device)
        self.dones = torch.zeros(buffer_size, device=self.device)
        self.logprobs = torch.zeros(buffer_size, device=self.device)
        self.values = torch.zeros(buffer_size, device=self.device)

        # Computed later
        self.advantages = torch.zeros(buffer_size, device=self.device)
        self.returns = torch.zeros(buffer_size, device=self.device)

        self.ptr = 0

    def store(self, state, action, reward, done, logprob, value):
        """Store one transition."""

        if self.ptr >= self.buffer_size:
            raise ValueError("Buffer overflow")

        # inputs are coming from network so they follow (B, dim) shape 
        # state - allow [1,21,9] -> [21,9]
        # action - allow [1, act_dim] -> [act_dim]
        # logprob, value - allow [1] -> []
        # value - allow [1,1] -> []

        state = state.to(self.device)
        action = action.to(self.device)
        logprob = logprob.to(self.device).squeeze()
        value = value.to(self.device).squeeze()

        # action: allow [1, act_dim] -> [act_dim]
        if action.dim() == 2 and action.shape[0] == 1:
            action = action.squeeze(0)

        # state: allow [1,21,9] -> [21,9]
        if state.dim() == 3 and state.shape[0] == 1:
            state = state.squeeze(0)

        self.states[self.ptr] = state
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward if not torch.is_tensor(reward) else reward.to(self.device).squeeze()
        self.dones[self.ptr] = done if not torch.is_tensor(done) else done.to(self.device).squeeze()
        self.logprobs[self.ptr] = logprob
        self.values[self.ptr] = value

        self.ptr += 1

    def compute_advantages(self, last_value, gamma, gae_lambda):
        """Compute GAE advantages and returns."""
        advantage = 0
        last_value = last_value.to(self.device).squeeze() if torch.is_tensor(last_value) else torch.tensor(last_value, device=self.device)

        for t in reversed(range(self.buffer_size)):
            if t == self.buffer_size - 1:
                next_value = last_value
            else:
                next_value = self.values[t + 1]

            delta = (
                self.rewards[t]
                + gamma * next_value * (1 - self.dones[t])
                - self.values[t]
            )

            advantage = delta + gamma * gae_lambda * (1 - self.dones[t]) * advantage
            self.advantages[t] = advantage

        self.returns = self.advantages + self.values

        self.advantages = (self.advantages - self.advantages.mean()) / (
            self.advantages.std() + 1e-8
        )

    def get_minibatches(self, minibatch_size):
        """Yield shuffled minibatches."""
        indices = torch.randperm(self.buffer_size, device=self.device)

        for start in range(0, self.buffer_size, minibatch_size):
            end = min(start + minibatch_size, self.buffer_size)
            batch_idx = indices[start:end]

            yield (
                self.states[batch_idx],
                self.actions[batch_idx],
                self.logprobs[batch_idx],
                self.returns[batch_idx],
                self.advantages[batch_idx],
            )

    def clear(self):
        """Reset buffer pointer."""
        self.ptr = 0

