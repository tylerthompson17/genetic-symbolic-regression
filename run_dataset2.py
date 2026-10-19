import numpy as np
import pandas as pd
import gp
import tree
from tree import evaluate

df = pd.read_csv("dataset2.csv", skiprows=1, names=["x1", "x2", "x3", "y"], dtype=float)

df["x1"] = df["x1"] / 1000000
df["x2"] = df["x2"] / 1000000

train_df = df.sample(n=5000, random_state=42)
test_df = df.drop(train_df.index)

x_train = {name: train_df[name].to_numpy() for name in ["x1", "x2", "x3"]}
y_train = train_df["y"].to_numpy()
x_test = {name: test_df[name].to_numpy() for name in ["x1", "x2", "x3"]}
y_test = test_df["y"].to_numpy()

def relative_error(formula, data):
    x_points, y_points = data
    y_hat = evaluate(formula, x_points)
    return np.mean(np.abs(y_points - y_hat) / (y_points + 1))

