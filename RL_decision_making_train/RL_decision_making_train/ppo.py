import torch
import torch.nn as nn

def compute_gae(rewards, masks, values, gamma=0.99, lam=0.95):
    advantages = torch.zeros_like(rewards)
    gae = 0
    for step in reversed(range(len(rewards))):
        delta = rewards[step] + gamma * values[step + 1] * masks[step] - values[step]
        gae = delta + gamma * lam * masks[step] * gae
        advantages[step] = gae
    returns = advantages + values[:-1]
    return returns, (advantages - advantages.mean()) / (advantages.std() + 1e-8)

def ppo_update(ac_model, optimizer, obs, actions, old_log_probs, returns, advantages, clip_eps=0.2, epochs=4, batch_size=64):
    dataset = torch.utils.data.TensorDataset(obs, actions, old_log_probs, returns, advantages)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    mse = nn.MSELoss()
    for _ in range(epochs):
        for b_obs, b_actions, b_old_logp, b_returns, b_adv in loader:
            logp, entropy, values = ac_model.evaluate_actions(b_obs, b_actions)
            ratio = (logp - b_old_logp).exp()
            surr1 = ratio * b_adv
            surr2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * b_adv
            policy_loss = -torch.min(surr1, surr2).mean()
            value_loss = mse(values, b_returns)
            entropy_loss = -entropy.mean()
            loss = policy_loss + 0.5 * value_loss + 0.01 * entropy_loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
