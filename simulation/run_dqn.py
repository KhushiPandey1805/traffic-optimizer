import traci
import random
import numpy as np
import pandas as pd

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

def train_step():

    if len(memory) < batch_size:
        return

    batch = random.sample(memory, batch_size)

    states = []
    targets = []

    for state, action, reward, next_state in batch:

        state_tensor = state_to_tensor(state)
        next_tensor = state_to_tensor(next_state)

        with torch.no_grad():
            target = model(state_tensor).clone()

            target[action] = (
                reward +
                gamma * torch.max(target_model(next_tensor))
            )

        states.append(state_tensor)
        targets.append(target)

    states = torch.stack(states)
    targets = torch.stack(targets)

    predictions = model(states)

    loss = criterion(predictions, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

def get_state():

    ns = (
        traci.edge.getLastStepHaltingNumber("n2c")
        +
        traci.edge.getLastStepHaltingNumber("s2c")
    )

    ew = (
        traci.edge.getLastStepHaltingNumber("e2c")
        +
        traci.edge.getLastStepHaltingNumber("w2c")
    )

    ns = min(ns // 2, 10)
    ew = min(ew // 2, 10)

    phase = current_phase // 2

    return (ns, ew, phase)

def get_reward():

    north = traci.edge.getWaitingTime("n2c")
    south = traci.edge.getWaitingTime("s2c")
    east  = traci.edge.getWaitingTime("e2c")
    west  = traci.edge.getWaitingTime("w2c")

    return -(
        north +
        south +
        east +
        west
    )

model = DQN()

target_model=DQN()

target_model.load_state_dict(model.state_dict())

target_model.eval()

training_log=[]

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

min_green = 10

best_reward=float("-inf")

for episode in range(200):

    if (episode+1)%10==0:
        target_model.load_state_dict(model.state_dict())
        print("Target network updated.")

    traci.start(sumoCmd)

    tls = traci.trafficlight.getIDList()[0]

    current_phase = 0
    last_switch = 0

    traci.simulationStep()

    state = get_state()

    total_reward = 0

    for step in range(500):

        action = choose_action(state)

        if step - last_switch >= min_green:

            if action == 0 and current_phase != 0:

                traci.trafficlight.setPhase(tls, 0)

                current_phase = 0
                last_switch = step

            elif action == 1 and current_phase != 2:

                traci.trafficlight.setPhase(tls, 2)

                current_phase = 2
                last_switch = step

        traci.simulationStep()

        reward = get_reward()

        next_state = get_state()

        total_reward += reward

        memory.append(

            (
                state,
                action,
                reward,
                next_state
            )

        )

        if step % 4 == 0:
            train_step()

        state = next_state

    traci.close()

    epsilon = max(
        epsilon_min,
        epsilon * epsilon_decay
    )

    print(
        f"Episode {episode:3d}"
        f" | Reward = {total_reward:.2f}"
        f" | Epsilon = {epsilon:.3f}"
    )

    training_log.append({
        "episode":episode,
        "reward":total_reward,
        "epsilon":epsilon
    })

    if total_reward>best_reward:
        best_reward=total_reward
        torch.save(model.state_dict(), "../results/best_dqn.pth")
        print(f"New best model! Reward={best_reward:.2f}")

pd.DataFrame(training_log).to_csv(
    "../results/dqn_training_log.csv",
    index=False
)

torch.save(
    model.state_dict(),
    "../results/dqn_model.pth"
)

print("Model saved.")