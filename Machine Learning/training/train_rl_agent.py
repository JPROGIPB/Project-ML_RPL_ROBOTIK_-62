"""
SEALEN - Reinforcement Learning Training Script
Train DQN agent for robot navigation and waste collection
"""

import os
import argparse
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from pathlib import Path
import json
from datetime import datetime

class OceanCleaningEnv(gym.Env):
    """Custom Environment for Ocean Cleaning Robot"""
    
    metadata = {'render.modes': ['human']}
    
    def __init__(self, grid_size=20, max_waste=10, max_steps=200):
        super(OceanCleaningEnv, self).__init__()
        
        self.grid_size = grid_size
        self.max_waste = max_waste
        self.max_steps = max_steps
        self.current_step = 0
        
        # State: [robot_x, robot_y, battery, nearest_waste_x, nearest_waste_y]
        self.observation_space = spaces.Box(
            low=0, 
            high=1, 
            shape=(5,), 
            dtype=np.float32
        )
        
        # Actions: 0=North, 1=South, 2=East, 3=West, 4=Collect
        self.action_space = spaces.Discrete(5)
        
        self.reset()
    
    def reset(self):
        """Reset environment to initial state"""
        # Robot starts at center
        self.robot_pos = [self.grid_size // 2, self.grid_size // 2]
        self.battery = 100
        self.current_step = 0
        self.collected_waste = 0
        
        # Generate random waste positions
        self.waste_positions = []
        for _ in range(self.max_waste):
            pos = [
                np.random.randint(0, self.grid_size),
                np.random.randint(0, self.grid_size)
            ]
            self.waste_positions.append(pos)
        
        return self._get_state()
    
    def step(self, action):
        """Execute action and return new state"""
        self.current_step += 1
        reward = 0
        
        # Execute action
        if action == 0:  # North
            self.robot_pos[1] = max(0, self.robot_pos[1] - 1)
            self.battery -= 1
            reward -= 0.1  # Movement penalty
            
        elif action == 1:  # South
            self.robot_pos[1] = min(self.grid_size - 1, self.robot_pos[1] + 1)
            self.battery -= 1
            reward -= 0.1
            
        elif action == 2:  # East
            self.robot_pos[0] = min(self.grid_size - 1, self.robot_pos[0] + 1)
            self.battery -= 1
            reward -= 0.1
            
        elif action == 3:  # West
            self.robot_pos[0] = max(0, self.robot_pos[0] - 1)
            self.battery -= 1
            reward -= 0.1
            
        elif action == 4:  # Collect
            # Check if waste is nearby
            collected = False
            for waste in self.waste_positions[:]:
                distance = self._distance(self.robot_pos, waste)
                if distance < 1.5:  # Collection radius
                    self.waste_positions.remove(waste)
                    self.collected_waste += 1
                    reward += 10  # Big reward for collecting
                    collected = True
                    break
            
            if not collected:
                reward -= 1  # Penalty for failed collection
            
            self.battery -= 2  # Collection uses more battery
        
        # Additional rewards/penalties
        if len(self.waste_positions) > 0:
            # Reward for getting closer to nearest waste
            nearest_dist = min([self._distance(self.robot_pos, w) 
                               for w in self.waste_positions])
            reward += (1.0 / (nearest_dist + 1)) * 0.5
        
        # Battery penalties
        if self.battery < 20:
            reward -= 2  # Low battery penalty
        
        # Check termination conditions
        done = False
        if self.battery <= 0:
            reward -= 50  # Big penalty for running out of battery
            done = True
        elif len(self.waste_positions) == 0:
            reward += 50  # Big reward for collecting all waste
            done = True
        elif self.current_step >= self.max_steps:
            reward -= 10  # Penalty for timeout
            done = True
        
        info = {
            'collected': self.collected_waste,
            'remaining': len(self.waste_positions),
            'battery': self.battery,
            'steps': self.current_step
        }
        
        return self._get_state(), reward, done, info
    
    def _get_state(self):
        """Get normalized state vector"""
        if len(self.waste_positions) > 0:
            # Find nearest waste
            nearest_waste = min(
                self.waste_positions,
                key=lambda w: self._distance(self.robot_pos, w)
            )
        else:
            nearest_waste = [0, 0]
        
        state = np.array([
            self.robot_pos[0] / self.grid_size,
            self.robot_pos[1] / self.grid_size,
            self.battery / 100,
            nearest_waste[0] / self.grid_size,
            nearest_waste[1] / self.grid_size
        ], dtype=np.float32)
        
        return state
    
    def _distance(self, pos1, pos2):
        """Calculate Euclidean distance"""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def render(self, mode='human'):
        """Render environment (optional)"""
        if mode == 'human':
            print(f"\nStep: {self.current_step}, Battery: {self.battery}")
            print(f"Robot: {self.robot_pos}, Waste collected: {self.collected_waste}/{self.max_waste}")
            print(f"Remaining waste: {len(self.waste_positions)}")

def parse_args():
    parser = argparse.ArgumentParser(description='Train DQN RL Agent')
    parser.add_argument('--timesteps', type=int, default=500000,
                        help='Total training timesteps')
    parser.add_argument('--grid_size', type=int, default=20,
                        help='Environment grid size')
    parser.add_argument('--max_waste', type=int, default=10,
                        help='Maximum waste items per episode')
    parser.add_argument('--learning_rate', type=float, default=1e-4,
                        help='Learning rate')
    parser.add_argument('--buffer_size', type=int, default=50000,
                        help='Replay buffer size')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size')
    parser.add_argument('--output_dir', type=str, default='../models/reinforcement',
                        help='Output directory')
    parser.add_argument('--name', type=str, default='dqn_ocean_cleaning',
                        help='Model name')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    output_path = Path(args.output_dir) / args.name
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("SEALEN - Reinforcement Learning Training")
    print("=" * 60)
    print(f"Environment: OceanCleaningEnv")
    print(f"Grid Size: {args.grid_size}x{args.grid_size}")
    print(f"Max Waste: {args.max_waste}")
    print(f"Total Timesteps: {args.timesteps:,}")
    print(f"Learning Rate: {args.learning_rate}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    # Create environment
    print("\n[1/4] Creating environment...")
    env = OceanCleaningEnv(
        grid_size=args.grid_size,
        max_waste=args.max_waste
    )
    env = Monitor(env, str(output_path / 'monitor'))
    
    # Create eval environment
    eval_env = OceanCleaningEnv(
        grid_size=args.grid_size,
        max_waste=args.max_waste
    )
    eval_env = Monitor(eval_env, str(output_path / 'eval_monitor'))
    
    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path=str(output_path / 'checkpoints'),
        name_prefix='dqn_model'
    )
    
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=str(output_path / 'best_model'),
        log_path=str(output_path / 'eval_logs'),
        eval_freq=5000,
        deterministic=True,
        render=False
    )
    
    # Create DQN model
    print("\n[2/4] Creating DQN model...")
    model = DQN(
        policy='MlpPolicy',
        env=env,
        learning_rate=args.learning_rate,
        buffer_size=args.buffer_size,
        learning_starts=1000,
        batch_size=args.batch_size,
        tau=1.0,
        gamma=0.99,
        train_freq=4,
        gradient_steps=1,
        target_update_interval=1000,
        exploration_fraction=0.1,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.02,
        policy_kwargs=dict(net_arch=[256, 256]),
        verbose=1,
        tensorboard_log=str(output_path / 'tensorboard')
    )
    
    # Train model
    print("\n[3/4] Starting training...")
    model.learn(
        total_timesteps=args.timesteps,
        callback=[checkpoint_callback, eval_callback],
        log_interval=100
    )
    
    # Save final model
    print("\n[4/4] Saving final model...")
    model.save(output_path / f'{args.name}_final')
    
    # Test model
    print("\n" + "=" * 60)
    print("TESTING MODEL")
    print("=" * 60)
    
    total_rewards = []
    success_count = 0
    
    for episode in range(100):
        obs = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
        
        total_rewards.append(episode_reward)
        if info['remaining'] == 0:
            success_count += 1
    
    avg_reward = np.mean(total_rewards)
    success_rate = success_count / 100
    
    print(f"\nAverage Reward: {avg_reward:.2f}")
    print(f"Success Rate: {success_rate:.1%}")
    print(f"Min Reward: {np.min(total_rewards):.2f}")
    print(f"Max Reward: {np.max(total_rewards):.2f}")
    print("=" * 60)
    
    # Save results
    results = {
        'model_name': args.name,
        'timesteps': args.timesteps,
        'grid_size': args.grid_size,
        'max_waste': args.max_waste,
        'learning_rate': args.learning_rate,
        'avg_reward': float(avg_reward),
        'success_rate': float(success_rate),
        'min_reward': float(np.min(total_rewards)),
        'max_reward': float(np.max(total_rewards)),
        'trained_on': datetime.now().isoformat()
    }
    
    with open(output_path / 'results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Training completed successfully!")
    print(f"📁 Model saved to: {output_path}")
    
    # Performance check
    if success_rate >= 0.80:
        print("🎉 Target success rate (>80%) achieved!")
    else:
        print(f"⚠️ Success rate is {success_rate:.1%}, target is 80%")
        print("   Consider training for more timesteps or tuning hyperparameters")

if __name__ == '__main__':
    main()
