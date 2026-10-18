from Tree import *

NUM_TREES = 100 # initial number of random trees
NUM_GEN = 10_000 # total recurrences

def fit():
    trees = generate_trees(NUM_TREES)

    for i in range(NUM_GEN):
        # 1. Get fitness for every tree
        # 2. Select a certain pop of trees
        # 3. Mutate a certain pop of trees
        # 4. Crossover a certain pop of trees
        pass
