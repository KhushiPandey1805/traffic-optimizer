import traci
import random
import numpy as np

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

    # compress values into bins

    ns = min(ns//2,10)
    ew = min(ew//2,10)

    return ns, ew

sumoCmd=["sumo-gui","-c","config.sumocfg"]

# Q-table
Q = np.zeros((11,11,2))

# learning parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

current_phase = 0

def choose_action(state):

    if random.random() < epsilon:
        return random.randint(0,1)

    return np.argmax(
        Q[state[0],state[1]]
    )

def get_reward():

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

    return -(ns+ew)

for episode in range(50):

    epsilon=max(0.01, epsilon*0.95)

    print(f"\nEpisode {episode}, epsilon={epsilon:.3f}")

    traci.start(["sumo", "-c", "config.sumocfg"])

    tls = traci.trafficlight.getIDList()[0]

    total_reward = 0

    current_phase=0

    for step in range(500):

        traci.simulationStep()

        state = get_state()

        action = choose_action(state)

        # Apply action
        if action == 0 and current_phase!=0:
            traci.trafficlight.setPhase(tls,0)
            current_phase=0

        elif action==1 and current_phase!=2:
            traci.trafficlight.setPhase(tls,2)
            current_phase=2

        reward = get_reward()

        total_reward += reward

        next_state = get_state()

        old_q = Q[
            state[0],
            state[1],
            action
        ]

        future_q = np.max(
            Q[
                next_state[0],
                next_state[1]
            ]
        )

        Q[
            state[0],
            state[1],
            action
        ] = old_q + alpha * (
            reward
            + gamma*future_q
            - old_q
        )

    traci.close()

    print(
        f"Total reward: {total_reward}"
    )

print("\nTraining complete")

np.save("../results/qtable.npy", Q)

print("Q-table saved")