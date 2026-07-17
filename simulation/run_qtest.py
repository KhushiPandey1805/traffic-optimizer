import traci
import numpy as np
import pandas as pd
import sys

Q = np.load("../results/qtable.npy")

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

    phase = 0 if current_phase == 0 else 1

    return ns, ew, phase


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

tls=traci.trafficlight.getIDList()[0]

current_phase=0
min_green = 10
last_switch = 0

data=[]

for step in range(500):

    traci.simulationStep()

    state=get_state()

    action=np.argmax(
        Q[
            state[0],
            state[1],
            state[2]
        ]
    )

    if step-last_switch>=min_green:
        if action==0 and current_phase!=0:

            traci.trafficlight.setPhase(
                tls,
                0
            )

            current_phase=0
            last_switch=step


        elif action==1 and current_phase!=2:

            traci.trafficlight.setPhase(
                tls,
                2
            )

            current_phase=2
            last_switch=step


    vehicles=traci.vehicle.getIDList()

    total_wait=0

    for vehicle in vehicles:

        total_wait += (
            traci.vehicle.getWaitingTime(
                vehicle
            )
        )

    data.append([
        step,
        len(vehicles),
        total_wait
    ])


traci.close()


df=pd.DataFrame(
    data,
    columns=[
        "time",
        "cars",
        "wait"
    ]
)

df.to_csv(
    f"../results/qlearning_seed{seed}.csv",
    index=False
)

print("RL results saved")