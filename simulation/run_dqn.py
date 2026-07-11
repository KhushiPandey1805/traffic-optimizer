import traci
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

from collections import deque


class DQN(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(3, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            nn.Linear(64, 2)

        )

    def forward(self, x):

        return self.network(x)

def state_to_tensor(state):

    return torch.tensor(
        state,
        dtype=torch.float32
    )

def choose_action(state):

    if random.random() < epsilon:
        return random.randint(0, 1)

    x = state_to_tensor(state)

    with torch.no_grad():
        q_values = model(x)

    return torch.argmax(q_values).item()

def train_step(state, action, reward, next_state):

    state_tensor = state_to_tensor(state)
    next_tensor = state_to_tensor(next_state)

    prediction = model(state_tensor)[action]

    with torch.no_grad():
        target = reward + gamma * torch.max(model(next_tensor))

    loss = criterion(prediction, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

model = DQN()



optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)

memory = deque(maxlen=10000)

gamma = 0.99

epsilon = 1.0

epsilon_decay = 0.995

epsilon_min = 0.05

batch_size = 32

criterion = nn.MSELoss()

sumoCmd = [
    "sumo",
    "-c",
    "../config.sumocfg"
]

for episode in range(200):

    traci.start(sumoCmd)

    tls = traci.trafficlight.getIDList()[0]

    current_phase = 0

    state = get_state()

    total_reward = 0

    for step in range(500):

        pass

    traci.close()

    epsilon = max(
        epsilon_min,
        epsilon * epsilon_decay
    )

    print(
        f"Episode {episode}, epsilon={epsilon:.3f}"
    )
