"""
Custom RL environment (Gym-like) for SEALEN simulation.
Provides obs -> action -> reward loop.
"""
import numpy as np
from math import sqrt
from data_generator import RLDataGenerator

class SealenEnv:
    def __init__(self, grid_size=100, num_waste=10, max_steps=2000):
        self.grid_size = grid_size
        self.num_waste = num_waste
        self.max_steps = max_steps
        self.generator = RLDataGenerator(grid_size=grid_size, num_waste=num_waste)
        self.reset()

    def reset(self):
        self.generator.reset()
        self.steps = 0
        state = self.generator.get_state()
        return self._state_to_obs(state)

    def _state_to_obs(self, state):
        # Return a flat numpy array observation
        obs = np.array([
            state['robot_x'],
            state['robot_y'],
            state['battery'],
            state['nearest_waste_x'],
            state['nearest_waste_y'],
            state['distance_to_waste'],
            state['mission_progress']
        ], dtype=np.float32)
        return obs

    def step(self, action):
        old_state, action, reward, new_state, done = self.generator.step(action)
        self.steps += 1
        if self.steps >= self.max_steps:
            done = True
        return self._state_to_obs(new_state), reward, done, {'state': new_state}
