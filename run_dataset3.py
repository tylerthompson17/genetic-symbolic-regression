import pandas as pd
import gp
import tree

df = pd.read_csv("dataset3.csv")

test_df = df.sample(n=20000, random_state=42)
train_df = df.drop(test_df.index)

tree.IS_UNARY = True
tree.REAL_CONSTANTS = False
tree.MAX_DEPTH = 12
gp.SIZE_PENALTY = 0.001 # bigger penalty size
gp.CROSSOVER_P = .7 # 20% mutation


x_train, y_train = train_df["x"].to_numpy(), train_df["f(x)"].to_numpy()
x_test,  y_test  = test_df["x"].to_numpy(),  test_df["f(x)"].to_numpy()

result = None # the best run by test error
best_error = float("inf")

for run in range(10):
    formula = gp.fit((x_train, y_train))
    error = gp.get_fitness(formula, (x_test, y_test))
    print(run, error, tree.to_string(formula))
    if error < best_error:
        result = formula
        best_error = error

print("best formula:", tree.to_string(result))
print("train error:", gp.get_fitness(result, (x_train, y_train)))
print("test error:", best_error)
