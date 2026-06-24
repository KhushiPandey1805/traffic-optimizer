import traci

sumoCmd = ["sumo-gui", "-c", "config.sumocfg"]

traci.start(sumoCmd)

tls = traci.trafficlight.getIDList()[0]

current_phase = 0
min_green = 15 
last_switch = 0

for step in range(300):

    traci.simulationStep()

    # Queue lengths
    ns = (
        traci.edge.getLastStepHaltingNumber("n2c")
        + traci.edge.getLastStepHaltingNumber("s2c")
    )

    ew = (
        traci.edge.getLastStepHaltingNumber("e2c")
        + traci.edge.getLastStepHaltingNumber("w2c")
    )

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

traci.close()