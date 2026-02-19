import torch

class AgentPPO:
    def __init__(
            self,
            network,
            optimizer,
            rollout_buffer,
            no_epoch,
            clip_eps,
            vf_coeff,
            ent_coeff,
            max_grad_norm,
            minibatch_size,
            gamma,
            gae_lambda
            ):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = network.to(self.device)
        self.optimizer = optimizer
        self.rollout_buffer = rollout_buffer
        self.no_epoch = no_epoch

        self.clip_eps = clip_eps
        self.vf_coeff = vf_coeff
        self.ent_coeff = ent_coeff
        self.max_grad_norm = max_grad_norm
        self.minibatch_size = minibatch_size
       

    def get_action(self, state):
        """Knowing state find action using policy network."""
        if not torch.is_tensor(state):
            raise TypeError("state must be a torch.Tensor")

        state = state.to(self.device)
        if state.dim() == 2:
            state = state.unsqueeze(0)

        # Assumes your network returns: action, logprob, value (and maybe entropy internally)
        # If your network returns (mean, log_std, value) instead, keep your previous get_action.
        action, logprob, value = self.network(state)
        action = action.detach()
        logprob = logprob.detach()
        value = value.detach() 

        return action, logprob, value

    def update(self):
        """
        calculate and clip policy ratio
        calculate policy loss, value_loss, entropy loss,
        gradient, back_propagation
        """
        self.network.train()
        epochs = 0

        while epochs < self.no_epoch:

            for state, action, log_p_old, returns, advantages in \
                    self.rollout_buffer.get_minibatches(self.minibatch_size):

                state = state.to(self.device)
                action = action.to(self.device)
                log_p_old = log_p_old.to(self.device)
                returns = returns.to(self.device)
                advantages = advantages.to(self.device)

                # network must provide: logp_new, entropy, value for given (state, action)
                logp, entropy, value = self.network.evaluate(state, action)

                # ratio = exp(new - old)
                ratio = torch.exp(logp - log_p_old)

                # value loss
                value = value.squeeze(-1)
                value_loss = torch.mean((returns - value) ** 2)

                # policy loss (clipped surrogate)
                obj_1 = ratio * advantages
                obj_2 = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * advantages
                policy_loss = -torch.mean(torch.min(obj_1, obj_2))

                # entropy bonus
                entropy_loss = -torch.mean(entropy)

                total_loss = policy_loss + \
                             self.vf_coeff * value_loss + \
                             self.ent_coeff * entropy_loss

                self.optimizer.zero_grad()
                total_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()

            epochs += 1
