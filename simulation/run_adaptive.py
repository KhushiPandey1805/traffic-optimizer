import traci
import pandas as pd

from metrics import collect_metrics

sumoCmd = ["sumo-gui", "-c", "../config.sumocfg"]

traci.start(sumoCmd)

tls = traci.trafficlight.getIDList()[0]

data=[]

current_phase = 0
min_green = 15 
last_switch = 0

for step in range(500):

    traci.simulationStep()

    north = traci.edge.getWaitingTime("n2c")
    south = traci.edge.getWaitingTime("s2c")
    east  = traci.edge.getWaitingTime("e2c")
    west  = traci.edge.getWaitingTime("w2c")

    ns = north + south
    ew = east + west

    # Wait at least min_green steps before changing
    if step - last_switch >= min_green:

        # Phase 0 = NS green
        # Phase 2 = EW green

        if ns > ew and current_phase != 0:

            traci.trafficlight.setPhase(tls,0)

            current_phase = 0
            last_switch = step

            print(
                f"Step {step}: "
                f"Switching to NS "
                f"(NS={ns}, EW={ew})"
            )

        elif ew > ns and current_phase != 2:

            traci.trafficlight.setPhase(tls,2)

            current_phase = 2
            last_switch = step

            print(
                f"Step {step}: "
                f"Switching to EW "
                f"(NS={ns}, EW={ew})"
            )
    m=collect_metrics()

    data.append(
        [step,m["cars"],m["wait"],m["queue"]]
    )

traci.close()

df=pd.DataFrame(
    data,
    columns=[
        "time",
        "cars",
        "wait",
        "queue"
    ]
)

df.to_csv(
    "../results/adaptive.csv",
    index=False
)

print("Adaptive saved")