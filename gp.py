import random

import numpy as np

from tree import *

NUM_TREES = 100 # initial number of random trees
NUM_GEN = 10_000 # total recurrences
SELECTION_P = .1 # probability of individual to be reproduced
CROSSOVER_P = .88 # probability of individual to take part of crossovers
MUTATION_P = .02 # probability of individual to be mutated
TOURN_SIZE = 5 # tournament size
THRESHOLD = .00000001

def fit(data):
    trees = generate_trees(NUM_TREES)
    best_fitness = [] # each value at index n is the best fitness of generation n

    for i in range(NUM_GEN):
        next_gen = []
        fitn = []

        for tree in trees:
            fitn.append(get_fitness(tree, data))

        best = fitn.index(min(fitn))
        best_fitness.append(fitn[best])
        next_gen.append(trees[best]) # force best individual thru

        if best_fitness[-1] < THRESHOLD:
            return trees[best]

        for _ in range(NUM_TREES - 1):
            n = random.random()
            if n < SELECTION_P:
                next_gen.append(get_individual(trees, fitn))
            elif n < SELECTION_P + CROSSOVER_P:
                tree_a, tree_b = crossover(get_individual(trees, fitn), get_individual(trees, fitn))
                next_gen.append(tree_a if get_fitness(tree_a, data) < get_fitness(tree_b, data) else tree_b)
            else:
                next_gen.append(mutate(get_individual(trees, fitn)))

        trees = next_gen
    return trees[0] # this only works cus we force best individual into one slot

def get_fitness(tree, data):
    x_points, y_points = data
    y_hat = evaluate(tree, x_points)
    return np.mean((y_points - y_hat) ** 2)

def get_individual(trees, fitn):
    selected = random.sample(range(len(trees)), TOURN_SIZE)
    best = min(selected, key=lambda i: fitn[i])
    return trees[best]