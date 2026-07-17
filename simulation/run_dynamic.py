import traci
import pandas as pd
import sys

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

data=[]

current_phase = 0
next_switch = 0

for step in range(500):

    traci.simulationStep()

    north = traci.edge.getWaitingTime("n2c")
    south = traci.edge.getWaitingTime("s2c")
    east  = traci.edge.getWaitingTime("e2c")
    west  = traci.edge.getWaitingTime("w2c")

    ns = north + south
    ew = east + west

    vehicles = traci.vehicle.getIDList()

    total_wait = 0

    for vehicle in vehicles:
        total_wait += traci.vehicle.getWaitingTime(vehicle)

    data.append(
        [step,len(vehicles),total_wait]
    )

    if step >= next_switch:

        if ns >= ew:

            traci.trafficlight.setPhase(tls, 0)

            green_time = max(
                10,
                min(15 + int(ns / 20), 35)
            )

        else:

            traci.trafficlight.setPhase(tls, 2)

            green_time = max(
                10,
                min(15 + int(ew / 20), 35)
            )

        next_switch = step + green_time

        print(
            f"Step {step} | "
            f"NS Wait={ns:.1f} | "
            f"EW Wait={ew:.1f} | "
            f"Green={green_time}"
        )

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
    f"../results/dynamic_seed{seed}.csv",
    index=False
)