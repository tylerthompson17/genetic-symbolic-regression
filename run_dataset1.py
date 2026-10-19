import pandas as pd

from gp import fit

df = pd.read_csv("dataset1.csv")
x = df["x"].to_numpy()
y = df["f(x)"].to_numpy()
pairs = list(zip(x, y))
fit(pairs)