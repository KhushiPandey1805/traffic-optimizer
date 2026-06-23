import traci

sumoCmd = ["sumo-gui", "-c", "config.sumocfg"]

traci.start(sumoCmd)

tls = traci.trafficlight.getIDList()[0]

for step in range(300):

    traci.simulationStep()

    if step < 100:
        traci.trafficlight.setPhase(tls, 0)

    else:
        traci.trafficlight.setPhase(tls, 2)

traci.close()