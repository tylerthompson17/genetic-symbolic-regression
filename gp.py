import random

from Tree import *

NUM_TREES = 100 # initial number of random trees
NUM_GEN = 10_000 # total recurrences
SELECTION_P = .1 # probability of individual to be reproduced
CROSSOVER_P = .88 # probability of individual to take part of crossovers
MUTATION_P = .02 # probability of individual to be mutated

def fit():
    trees = generate_trees(NUM_TREES)
    best_fitness = [] # each value at index n is the best fitness of generation n

    for i in range(NUM_GEN):
        next_gen = []
        fitn = []

        for tree in trees:
            pass #fitn.append(get_fitness(tree))

        best = fitn.index(max(fitn))
        # consider if our fitness is good enough returning early
        best_fitness.append(fitn[best])
        next_gen.append(trees[best]) # force best individual thru

        for _ in range(NUM_TREES - 1):
            n = random.random()
            if n < SELECTION_P:
                pass # next_gen.append(get_individual(trees))
            elif n < SELECTION_P + CROSSOVER_P:
                # tree_a, tree_b =crossover(get_individual(trees), get_individual(trees))
                # next_gen.append(tree_a if get_fitness(tree_a) > get_fitness(tree_b) else tree_b)
                pass
            else:
                pass # next_gen.append(mutate(get_individual(trees)))

        trees = next_gen
    return best_fitness[len(best_fitness) - 1]