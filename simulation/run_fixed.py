import traci
import pandas as pd
import sys

from metrics import collect_metrics

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

for step in range(500):

    traci.simulationStep()

    if step%30==0:

        current=traci.trafficlight.getPhase(tls)

        if current==0:
            traci.trafficlight.setPhase(tls,2)

        else:
            traci.trafficlight.setPhase(tls,0)

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
    f"../results/fixed_seed{seed}.csv",
    index=False
)

print("Fixed saved")