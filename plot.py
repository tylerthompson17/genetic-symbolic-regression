import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tree import evaluate
from run_dataset3 import result

df = pd.read_csv("dataset3.csv")
right = df[df["x"] > -2]

fig, (full, zoom) = plt.subplots(1, 2, figsize=(12, 4))

full.scatter(df["x"], df["f(x)"], s=2, color="gray", label="data")
full.set_title("All x")

zoom.scatter(right["x"], right["f(x)"], s=2, color="gray", label="data")
zoom.set_title("Zoomed: x > -2")

for ax in (full, zoom):
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

xs = np.linspace(-5, 5, 1000)
ys = evaluate(result, xs)

full.plot(xs, ys, color="tab:blue", linewidth=2, label="GP formula")
full.set_ylim(df["f(x)"].min() * 1.2, df["f(x)"].max() * 1.2)

zoom.plot(xs[xs > -2], ys[xs > -2], color="tab:blue", linewidth=2, label="GP fomula")
zoom.set_ylim(right["f(x)"].min() - 1, right["f(x)"].max() + 1)

full.legend()
zoom.legend()

plt.tight_layout()
plt.show()