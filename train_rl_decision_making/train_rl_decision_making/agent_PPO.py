import torch
import torch.nn.functional as F

class AgentPPO:
    def __init__(
            self,
            network,
            optimizer,
            scheduler,
            rollout_buffer,
            no_epoch,
            clip_eps,
            vf_coeff,
            ent_coeff,
            max_grad_norm,
            minibatch_size,
            gamma,
            gae_lambda,
            chkpoint_path=None
            ):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = network.to(self.device)
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.rollout_buffer = rollout_buffer
        self.no_epoch = no_epoch
        self.clip_eps = clip_eps
        self.vf_coeff = vf_coeff
        self.ent_coeff = ent_coeff
        self.max_grad_norm = max_grad_norm
        self.minibatch_size = minibatch_size
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        assert any(p in self.optimizer.param_groups[0]["params"] for p in self.network.parameters())

        #load model if exists
        self.chkpoint_path = chkpoint_path
        if self.chkpoint_path is not None:
            try:
                self.load_model()
                print(f"Loaded model from {self.chkpoint_path}")
            except:
                print(f"No checkpoint found at {self.chkpoint_path}, starting from scratch.")  

    def get_action(self, state):
        """Knowing state find action using policy network."""
        if not torch.is_tensor(state):
            state = torch.tensor(state, dtype=torch.float32)
        #print("State in get_action:", state.shape)
        state = state.to(self.device)
        if state.dim() == 2:
            state = state.unsqueeze(0)

        #print("State in get_action:", state.shape)

        # Assumes your network returns: action, logprob, value (and maybe entropy internally)
        # If your network returns (mean, log_std, value) instead, keep your previous get_action.
        with torch.no_grad():
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

                print("")
                print("state size in update", state.shape)
                print("action size in update", action.shape)
                print("log_p_old size in update", log_p_old.shape)
                print("returns size in update", returns.shape)
                print("advantages size in update", advantages.shape)    
                state = state.to(self.device)
                action = action.to(self.device)
                log_p_old = log_p_old.to(self.device).detach()  # old log probs should not backpropagate
                returns = returns.to(self.device).detach()  # returns should not backpropagate
                advantages = advantages.to(self.device).detach()  # advantages should not backpropagate

                
                # network must provide: logp_new, entropy, value for given (state, action)
                #these return values should not be detached, as we need gradients for backprop                
                logp, entropy, value = self.network.evaluate(state, action)
                # print("logp size in update", logp.shape)
                # print("entropy size in update", entropy.shape)
                # print("value size in update", value.shape)
                logp = logp.squeeze(-1)
                value = value.squeeze(-1)
                entropy = entropy.squeeze(-1)
                # print("logp size in update", logp.shape)
                # print("entropy size in update", entropy.shape)
                # print("value size in update", value.shape)
                

                # ratio = exp(new - old) 
                # print("logp size in update", logp.shape)
                # print("log_p_old size in update", log_p_old.shape)               
                ratio = torch.exp(logp - log_p_old)

                # value loss 
                # print("returns size in update", returns.shape)
                # print("value size in update", value.shape)                              
                #value_loss = torch.mean((returns - value) ** 2)
                value_loss = F.huber_loss(value, returns, reduction='mean', delta=1.0)

                # policy loss (clipped surrogate)   
                # print("advantages size in update", advantages.shape)
                # print("ratio size in update", ratio.shape)            
                obj_1 = ratio * advantages
                obj_2 = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * advantages
                policy_loss = -torch.mean(torch.min(obj_1, obj_2))
                

                # entropy bonus
                entropy_loss = -torch.mean(entropy)
                
                # print("policy_loss in update", policy_loss.shape)
                # print("value_loss in update", value_loss.shape)
                # print("entropy_loss in update", entropy_loss.shape)
                total_loss = policy_loss + \
                             self.vf_coeff * value_loss + \
                             self.ent_coeff * entropy_loss
                

                self.optimizer.zero_grad()
                total_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()
                #print(state.shape, action.shape, log_p_old.shape, returns.shape, advantages.shape, logp.shape, entropy.shape, value.shape)

            epochs += 1
        
        #after update         
        with torch.no_grad():
                 self.network.log_std.clamp_(-5.0, 1.0)
        self.scheduler.step()

        
        return policy_loss.item(), value_loss.item(), total_loss.item(), entropy.mean().item()

    def save_model(self, path, env_step, episode_idx):
        checkpoint = {
        "model_state_dict": self.network.state_dict(),
        "optimizer_state_dict": self.optimizer.state_dict(),
        "episode": episode_idx,
        "total_steps": env_step,
        }

        torch.save(checkpoint, path)

    def load_model(self):
        checkpoint = torch.load(self.chkpoint_path, map_location=self.device, weights_only=True)
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])  
        self.network.load_state_dict(checkpoint["model_state_dict"])
        

        