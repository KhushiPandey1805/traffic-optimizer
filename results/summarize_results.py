import pandas as pd
import numpy as np
from pathlib import Path

controllers = [
    "fixed",
    "adaptive",
    "dynamic",
    "qlearning",
    "dqn"
]

NUM_SEEDS = range(10)

summary = []

for controller in controllers:

    average_waits = []
    maximum_waits = []

    for seed in NUM_SEEDS:

        file = Path(
            f"{controller}_seed{seed}.csv"
        )

        if not file.exists():
            print(f"Skipping missing file: {file}")
            continue

        df = pd.read_csv(file)

        average_waits.append(
            df["wait"].mean()
        )

        maximum_waits.append(
            df["wait"].max()
        )

    if len(average_waits) == 0:
        continue

    summary.append({

        "Controller": controller,

        "Mean Wait": round(np.mean(average_waits), 2),

        "Std Wait": round(np.std(average_waits, ddof=1), 2),

        "Mean Max Wait": round(np.mean(maximum_waits), 2),

        "Std Max Wait": round(np.std(maximum_waits, ddof=1), 2),

    })

summary = pd.DataFrame(summary)

summary.to_csv(
    "summary.csv",
    index=False
)

print(summary)