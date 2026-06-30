import pandas as pd
import matplotlib.pyplot as plt

fixed = pd.read_csv("fixed.csv")
adaptive = pd.read_csv("adaptive.csv")
dynamic = pd.read_csv("dynamic.csv")

fixed["smooth"] = fixed["wait"].rolling(10).mean()
adaptive["smooth"] = adaptive["wait"].rolling(10).mean()
dynamic["smooth"]=dynamic["wait"].rolling(10).mean()

print("Fixed avg wait:", fixed["wait"].mean())
print("Adaptive avg wait:", adaptive["wait"].mean())
print("Dynamic avg wait:", dynamic["wait"].mean())

print("Fixed max wait:", fixed["wait"].max())
print("Adaptive max wait:", adaptive["wait"].max())
print("Dynamic max wait:", dynamic["wait"].max())

plt.plot(
    fixed["time"],
    fixed["smooth"],
    label="Fixed"
)

plt.plot(
    adaptive["time"],
    adaptive["smooth"],
    label="Adaptive"
)

plt.plot(
    dynamic["time"],
    dynamic["smooth"],
    label="Dynamic"
)

plt.xlabel("Time")
plt.ylabel("Average Waiting Time")

plt.legend()

plt.savefig("comparison_smooth.png")

plt.show()