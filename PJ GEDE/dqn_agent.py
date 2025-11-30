"""
Simple DQN implementation for discrete action space (6 actions).
This is a compact educational implementation (not optimized).
"""
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from env import SealenEnv

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class QNet(nn.Module):
    def __init__(self, input_dim=7, output_dim=6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )
    def forward(self, x):
        return self.net(x)

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
    def push(self, s,a,r,ns,d):
        self.buffer.append((s,a,r,ns,d))
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        s,a,r,ns,d = zip(*batch)
        return np.vstack(s), np.array(a), np.array(r), np.vstack(ns), np.array(d)
    def __len__(self):
        return len(self.buffer)

def train(env, episodes=500, batch_size=64, gamma=0.99, lr=1e-3):
    qnet = QNet().to(DEVICE)
    target = QNet().to(DEVICE)
    target.load_state_dict(qnet.state_dict())
    opt = optim.Adam(qnet.parameters(), lr=lr)
    buf = ReplayBuffer()
    eps = 1.0
    eps_min = 0.05
    eps_decay = 0.995
    sync_every = 20
    for ep in range(episodes):
        obs = env.reset()
        total_r = 0
        done = False
        while not done:
            if random.random() < eps:
                action = random.randint(0,5)
            else:
                with torch.no_grad():
                    s = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
                    q = qnet(s).cpu().numpy()[0]
                    action = int(np.argmax(q))
            ns, r, done, info = env.step(action)
            buf.push(obs, action, r, ns, done)
            obs = ns
            total_r += r

            if len(buf) > batch_size:
                s_b, a_b, r_b, ns_b, d_b = buf.sample(batch_size)
                s_b = torch.tensor(s_b, dtype=torch.float32, device=DEVICE)
                ns_b = torch.tensor(ns_b, dtype=torch.float32, device=DEVICE)
                a_b = torch.tensor(a_b, dtype=torch.int64, device=DEVICE).unsqueeze(1)
                r_b = torch.tensor(r_b, dtype=torch.float32, device=DEVICE).unsqueeze(1)
                d_b = torch.tensor(d_b, dtype=torch.float32, device=DEVICE).unsqueeze(1)

                qvals = qnet(s_b).gather(1, a_b)
                with torch.no_grad():
                    next_q = target(ns_b).max(1)[0].unsqueeze(1)
                    target_q = r_b + gamma * next_q * (1 - d_b)
                loss = nn.MSELoss()(qvals, target_q)
                opt.zero_grad()
                loss.backward()
                opt.step()
        eps = max(eps*eps_decay, eps_min)
        if ep % sync_every == 0:
            target.load_state_dict(qnet.state_dict())
        if (ep+1) % 10 == 0:
            print(f"Episode {ep+1}/{episodes}  total_reward={total_r:.2f}  eps={eps:.3f}")
    return qnet

if __name__ == "__main__":
    env = SealenEnv()
    model = train(env, episodes=100)
    torch.save(model.state_dict(), "dqn_sealen.pth")
    print("Saved model: dqn_sealen.pth")
