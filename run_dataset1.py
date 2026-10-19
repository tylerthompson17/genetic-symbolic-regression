import pandas as pd

from gp import *

df = pd.read_csv("dataset1.csv")

test_df = df.sample(n=20000, random_state=42)
train_df = df.drop(test_df.index)

x_train, y_train = train_df["x"].to_numpy(), train_df["f(x)"].to_numpy()
x_test,  y_test  = test_df["x"].to_numpy(),  test_df["f(x)"].to_numpy()

result = fit((x_train, y_train))

print(f"Train mse: {get_fitness(result, (x_train, y_train))}")
print(f"Test mse: {get_fitness(result, (x_test, y_test))}")