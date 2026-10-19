import pandas as pd

df = pd.read_csv("dataset2.csv", skiprows=1, names=["x1", "x2", "x3", "y"], dtype=float)
print(df.shape)
print(df.head())