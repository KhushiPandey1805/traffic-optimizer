import pandas as pd

fixed = pd.read_csv("fixed.csv")
adaptive = pd.read_csv("adaptive.csv")
dynamic = pd.read_csv("dynamic.csv")
qlearning = pd.read_csv("qlearning.csv")
dqn= pd.read_csv("dqn.csv")

results = pd.DataFrame({

    "Method":[
        "Fixed",
        "Adaptive",
        "Dynamic",
        "Q-learning",
        "DQN"
    ],

    "Average Wait":[
        fixed["wait"].mean(),
        adaptive["wait"].mean(),
        dynamic["wait"].mean(),
        qlearning["wait"].mean(),
        dqn["wait"].mean()
    ],

    "Maximum Wait":[
        fixed["wait"].max(),
        adaptive["wait"].max(),
        dynamic["wait"].max(),
        qlearning["wait"].max(),
        dqn["wait"].max()
    ]
})

print(results)

results.to_csv(
    "summary.csv",
    index=False
)