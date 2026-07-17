import traci
import torch
import torch.nn as nn
import pandas as pd
import sys

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
    
model = DQN()

model.load_state_dict(
    torch.load(
        "../results/best_dqn.pth",
        map_location=torch.device("cpu")
    )
)

model.eval()

def state_to_tensor(state):

    return torch.tensor(
        state,
        dtype=torch.float32
    )

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

def choose_action(state):

    x = state_to_tensor(state)

    with torch.no_grad():

        q_values = model(x)

    return torch.argmax(q_values).item()

seed=0

if len(sys.argv)>1:
    seed=int(sys.argv[1])

sumoCmd = [
    "sumo",
    "-c",
    "../config.sumocfg",
    "--seed",
    str(seed)
]

traci.start(sumoCmd)

tls = traci.trafficlight.getIDList()[0]

current_phase = 0
last_switch = 0
min_green = 10

data = []

traci.simulationStep()

for step in range(500):

    state = get_state()

    action = choose_action(state)

    if step-last_switch>= min_green:

        if action==0 and current_phase!=0:
            traci.trafficlight.setPhase(tls, 0)

            current_phase=0
            last_switch=step
        
        elif action==1 and current_phase!=2:
            traci.trafficlight.setPhase(tls, 2)

            current_phase=2
            last_switch=step

    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    total_wait = 0

    for vehicle in vehicles:

        total_wait += traci.vehicle.getWaitingTime(vehicle)

    data.append([
        step,
        len(vehicles),
        total_wait
    ])

traci.close()

df = pd.DataFrame(
    data,
    columns=[
        "time",
        "cars",
        "wait"
    ]
)

df.to_csv(
    f"../results/dqn_seed{seed}.csv",
    index=False
)

print("DQN results saved.")