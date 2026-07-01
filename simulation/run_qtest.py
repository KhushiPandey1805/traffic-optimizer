import traci
import numpy as np
import pandas as pd

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

    ns=min(ns//2,10)
    ew=min(ew//2,10)

    return ns,ew


traci.start([
    "sumo-gui",
    "-c",
    "config.sumocfg"
])

tls=traci.trafficlight.getIDList()[0]

current_phase=0

data=[]

for step in range(500):

    traci.simulationStep()

    state=get_state()

    action=np.argmax(
        Q[
            state[0],
            state[1]
        ]
    )

    if action==0 and current_phase!=0:

        traci.trafficlight.setPhase(
            tls,
            0
        )

        current_phase=0


    elif action==1 and current_phase!=2:

        traci.trafficlight.setPhase(
            tls,
            2
        )

        current_phase=2


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