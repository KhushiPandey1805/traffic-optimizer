import traci
import pandas as pd

from metrics import collect_metrics

sumoCmd=["sumo-gui","-c","config.sumocfg"]

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
    "../results/fixed.csv",
    index=False
)

print("Fixed saved")