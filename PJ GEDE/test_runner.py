"""
Test runner to simulate episodes and print string outputs suitable for logging or sending.
"""
import json
from env import SealenEnv
from dqn_agent import QNet, train
import torch
import os
from data_generator import generate

def run_demo(episodes=5):
    env = SealenEnv()
    # Try to load trained model if available
    if os.path.exists("dqn_sealen.pth"):
        model = QNet()
        model.load_state_dict(torch.load("dqn_sealen.pth", map_location='cpu'))
        model.eval()
    else:
        print("No trained DQN found. Using heuristic policy and generating a small DQN by training 30 episodes.")
        model = train(env, episodes=30)

    for ep in range(episodes):
        obs = env.reset()
        done = False
        steps = 0
        while not done:
            s = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                out = model(s).numpy()[0]
            action = int(out.argmax())
            mapping = {0:'North',1:'South',2:'East',3:'West',4:'Collect',5:'ReturnHome'}
            obs, reward, done, info = env.step(action)
            # print a compact string output per step
            print(json.dumps({
                'episode': ep,
                'step': steps,
                'action': mapping[action],
                'reward': reward,
                'state': info['state']
            }))
            steps += 1

if __name__ == "__main__":
    run_demo(episodes=3)
