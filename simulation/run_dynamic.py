import traci
import pandas as pd

sumoCmd=["sumo-gui","-c","config.sumocfg"]

traci.start(sumoCmd)

tls = traci.trafficlight.getIDList()[0]

data=[]

current_phase = 0
next_switch = 0

for step in range(300):

    traci.simulationStep()

    ns = (
        traci.edge.getLastStepHaltingNumber("n2c")
        + traci.edge.getLastStepHaltingNumber("s2c")
    )

    ew = (
        traci.edge.getLastStepHaltingNumber("e2c")
        + traci.edge.getLastStepHaltingNumber("w2c")
    )

    vehicles = traci.vehicle.getIDList()

    total_wait = 0

    for vehicle in vehicles:
        total_wait += traci.vehicle.getWaitingTime(vehicle)

    data.append(
        [step,len(vehicles),total_wait]
    )

    if step >= next_switch:

        if ns > ew:

            traci.trafficlight.setPhase(tls,0)

            green_time = min(
                15 + int(ns * 0.5),
                30
            )

        else:

            traci.trafficlight.setPhase(tls,2)

            green_time = min(
                15 + int(ew * 0.5),
                30
            )

        next_switch = step + green_time

        print(
            f"Step {step}"
            f" NS={ns}"
            f" EW={ew}"
            f" Green={green_time}"
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
    "../results/dynamic.csv",
    index=False
)