import traci

def collect_metrics():

    vehicles = traci.vehicle.getIDList()

    total_wait = 0

    for vehicle in vehicles:
        total_wait += traci.vehicle.getWaitingTime(vehicle)

    ns = (
        traci.edge.getLastStepHaltingNumber("n2c")
        + traci.edge.getLastStepHaltingNumber("s2c")
    )

    ew = (
        traci.edge.getLastStepHaltingNumber("e2c")
        + traci.edge.getLastStepHaltingNumber("w2c")
    )

    queue = ns + ew

    return {
        "cars": len(vehicles),
        "wait": total_wait,
        "queue": queue
    }