"""
RL Data Generator for SEALEN project
Generates dummy episodes/transitions for training/testing.
"""
import numpy as np
import random
import json
from math import sqrt

class RLDataGenerator:
    def __init__(self, grid_size=100, num_waste=10):
        self.grid_size = grid_size
        self.num_waste = num_waste
        self.reset()

    def reset(self):
        self.robot_pos = [self.grid_size // 2, self.grid_size // 2]
        self.battery = 100.0
        self.waste_positions = [
            [random.randint(5, self.grid_size-5), random.randint(5, self.grid_size-5)]
            for _ in range(self.num_waste)
        ]
        self.collected_waste = 0
        self.steps = 0

    @staticmethod
    def distance(a, b):
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def get_nearest_waste(self):
        if not self.waste_positions:
            return [0,0]
        return min(self.waste_positions, key=lambda w: self.distance(self.robot_pos, w))

    def get_state(self):
        nearest = self.get_nearest_waste()
        dist = self.distance(self.robot_pos, nearest)
        progress = (self.collected_waste / max(1, self.num_waste)) * 100
        return {
            'robot_x': int(self.robot_pos[0]),
            'robot_y': int(self.robot_pos[1]),
            'battery': float(self.battery),
            'nearest_waste_x': int(nearest[0]),
            'nearest_waste_y': int(nearest[1]),
            'distance_to_waste': float(dist),
            'mission_progress': float(progress)
        }

    def step(self, action):
        """Take action and return (state, action, reward, next_state, done)"""
        old_state = self.get_state()
        reward = 0.0
        done = False

        # move
        if action == 0:  # North
            self.robot_pos[1] = max(0, self.robot_pos[1] - 1)
        elif action == 1:  # South
            self.robot_pos[1] = min(self.grid_size-1, self.robot_pos[1] + 1)
        elif action == 2:  # East
            self.robot_pos[0] = min(self.grid_size-1, self.robot_pos[0] + 1)
        elif action == 3:  # West
            self.robot_pos[0] = max(0, self.robot_pos[0] - 1)
        elif action == 4:  # Collect
            # collect if within 1.5 units
            for w in self.waste_positions[:]:
                if self.distance(self.robot_pos, w) < 1.5:
                    self.waste_positions.remove(w)
                    self.collected_waste += 1
                    reward += 10.0
        elif action == 5:  # Return Home
            home = [self.grid_size//2, self.grid_size//2]
            if self.robot_pos[0] > home[0]:
                self.robot_pos[0] -= 1
            elif self.robot_pos[0] < home[0]:
                self.robot_pos[0] += 1
            if self.robot_pos[1] > home[1]:
                self.robot_pos[1] -= 1
            elif self.robot_pos[1] < home[1]:
                self.robot_pos[1] += 1

        # battery/time penalty
        self.battery -= 0.5
        reward -= 0.5

        # proximity bonus
        nearest = self.get_nearest_waste()
        dist = self.distance(self.robot_pos, nearest)
        if dist < 5:
            reward += 2.0

        # done conditions
        self.steps += 1
        if self.battery <= 0:
            reward -= 50.0
            done = True
        if len(self.waste_positions) == 0:
            reward += 50.0
            done = True
        if self.steps > 2000:
            done = True

        new_state = self.get_state()
        return old_state, action, reward, new_state, done

def generate(num_episodes=1000, save_json=True, save_csv=True, out_path="rl_training_data.json"):
    import pandas as pd
    g = RLDataGenerator()
    transitions = []
    for ep in range(num_episodes):
        g.reset()
        while True:
            # simple heuristic policy for data gen
            s = g.get_state()
            dx = s['nearest_waste_x'] - s['robot_x']
            dy = s['nearest_waste_y'] - s['robot_y']
            if abs(dx) < 2 and abs(dy) < 2:
                action = 4
            elif abs(dx) > abs(dy):
                action = 2 if dx > 0 else 3
            else:
                action = 1 if dy > 0 else 0

            old, a, r, new, done = g.step(action)
            # create a simple human-readable description in Indonesian
            def describe(old_state, action, reward, new_state, done):
                # mapping action -> text
                mapping = {0: 'Utara', 1: 'Selatan', 2: 'Timur', 3: 'Barat', 4: 'Kumpulkan', 5: 'Kembali ke base'}
                act_text = mapping.get(action, str(action))
                rx = old_state.get('robot_x')
                ry = old_state.get('robot_y')
                batt = old_state.get('battery')
                nx = old_state.get('nearest_waste_x')
                ny = old_state.get('nearest_waste_y')
                dist = old_state.get('distance_to_waste')
                prog = old_state.get('mission_progress')
                done_text = 'Ya' if done else 'Tidak'
                # build a short sentence describing the situation
                return (f"Episode {ep} langkah {g.steps}: Robot di ({rx},{ry}), baterai {batt:.1f}%, "
                        f"sampah terdekat di ({nx},{ny}) jarak {dist:.2f}, progress {prog:.1f}%. "
                        f"Aksi: {act_text}, reward: {reward:.2f}, selesai: {done_text}.")

            desc = describe(old, a, r, new, done)

            transitions.append({
                'episode': ep, 'step': g.steps,
                'state': old, 'action': a, 'reward': r, 'next_state': new, 'done': done,
                'description': desc
            })
            if done:
                break

    if save_json:
        with open(out_path, 'w') as f:
            json.dump(transitions, f, indent=2)
    if save_csv:
        rows = []
        for t in transitions:
            st = t['state']
            rows.append({
                'episode': t['episode'],
                'step': t['step'],
                'robot_x': st['robot_x'],
                'robot_y': st['robot_y'],
                'battery': st['battery'],
                'nearest_waste_x': st['nearest_waste_x'],
                'nearest_waste_y': st['nearest_waste_y'],
                'distance': st['distance_to_waste'],
                'progress': st['mission_progress'],
                'action': t['action'],
                'reward': t['reward'],
                'done': t['done'],
                'description': t.get('description')
            })
        df = pd.DataFrame(rows)
        df.to_csv(out_path.replace('.json', '.csv'), index=False)
    return transitions

if __name__ == "__main__":
    print("Generating sample data (100 episodes)...")
    generate(num_episodes=100, out_path="rl_training_data.json")
    print("Done.")
