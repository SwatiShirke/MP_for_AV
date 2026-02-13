import gym
import numpy as np
try:
    import carla
    _HAS_CARLA = True
except Exception:
    _HAS_CARLA = False

from gym import spaces

class CarlaEnv(gym.Env):
    def __init__(self, host='localhost', port=2000, discrete=True):
        super().__init__()
        self.discrete = discrete
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(24,), dtype=np.float32)
        if self.discrete:
            self.action_space = spaces.Discrete(3)
        else:
            self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self._mock = not _HAS_CARLA
        self._episode_steps = 0

    def reset(self):
        self._episode_steps = 0
        if self._mock:
            return np.zeros(self.observation_space.shape, dtype=np.float32)
        world = self._get_world()
        obs = np.zeros(self.observation_space.shape, dtype=np.float32)
        return obs

    def step(self, action):
        self._episode_steps += 1
        if self._mock:
            obs = np.zeros(self.observation_space.shape, dtype=np.float32)
            reward = 0.0
            done = self._episode_steps >= 200
            info = {}
            return obs, reward, done, info
        obs = np.zeros(self.observation_space.shape, dtype=np.float32)
        reward = 0.0
        done = self._episode_steps >= 1000
        info = {}
        return obs, reward, done, info

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def _get_world(self):
        if self._mock:
            return None
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        return client.get_world()
