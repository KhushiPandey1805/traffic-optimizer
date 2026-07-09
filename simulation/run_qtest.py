import traci
import numpy as np
import pandas as pd

Q = np.load("../results/qtable.npy")

def get_state():

    north = min(
        traci.edge.getLastStepHaltingNumber("n2c") // 2,
        10
    )

    south = min(
        traci.edge.getLastStepHaltingNumber("s2c") // 2,
        10
    )

    east = min(
        traci.edge.getLastStepHaltingNumber("e2c") // 2,
        10
    )

    west = min(
        traci.edge.getLastStepHaltingNumber("w2c") // 2,
        10
    )

    return north, south, east, west


traci.start([
    "sumo-gui",
    "-c",
    "../config.sumocfg"
])

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
            state[2],
            state[3]
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
    "../results/qlearning.csv",
    index=False
)

print("RL results saved")