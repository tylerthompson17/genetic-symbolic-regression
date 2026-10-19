import pandas as pd
import gp
import tree

df = pd.read_csv("dataset3.csv")

test_df = df.sample(n=20000, random_state=42)
train_df = df.drop(test_df.index)

tree.IS_UNARY = True

x_train, y_train = train_df["x"].to_numpy(), train_df["f(x)"].to_numpy()
x_test,  y_test  = test_df["x"].to_numpy(),  test_df["f(x)"].to_numpy()

result = gp.fit((x_train, y_train))

print(tree.to_string(result))
print("train error:", gp.get_fitness(result, (x_train, y_train)))
print("test error:", gp.get_fitness(result, (x_test, y_test)))
