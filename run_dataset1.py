import pandas as pd

from gp import fit

df = pd.read_csv("dataset1.csv")

test_df = df.sample(n=20000, random_state=42)
train_df = df.drop(test_df.index)

x_train, y_train = train_df["x"].to_numpy(), train_df["f(x)"].to_numpy()
x_test,  y_test  = test_df["x"].to_numpy(),  test_df["f(x)"].to_numpy()

train_pairs = list(zip(x_train, y_train))
test_pairs  = list(zip(x_test, y_test))

print(fit((x_train, y_train)))