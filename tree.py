import random
import numpy as np

OPERATORS = ['+','-','/','*']
VARIABLES = ["x"] # for dataset2 we need a list of x's
REAL_CONSTANTS = False # dataset2 requires real numbers instead of integers
MAX_INITIAL_DEPTH = 3
MAX_DEPTH = 8

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def rand_leaf():
    rand = random.randint(0, 1)
    if rand == 0:
        if REAL_CONSTANTS:
            return Node(random.uniform(-5, 5))
        return Node(random.randint(-5, 5))
    return Node(random.choice(VARIABLES))

def rand_tree(depth = 0):
    rand = random.randint(-1, 1)
    if depth >= MAX_INITIAL_DEPTH or (depth > 0 and rand >= 0):
        return rand_leaf()
    return Node(
        random.choice(OPERATORS),
        rand_tree(depth + 1),
        rand_tree(depth + 1)
    )

def generate_trees(num):
    trees = []
    for i in range(num):
        trees.append(rand_tree())
    return trees

def mutate(tree):
    if REAL_CONSTANTS and random.random() < 0.5: # if using dataset2, half of the times nudge the values 
        return nudge(tree)                       # instead of mutating them.

    idx = random.randint(1, count_nodes(tree))
    if random.randint(-1, 1) == -1:
        mutated = replace_subtree(tree, idx, rand_tree())
    else:
        mutated = replace_subtree(tree, idx, rand_leaf())
    if get_depth(mutated) > MAX_DEPTH:
        return tree
    return mutated

def nudge(tree):
    constants = [i for i in range(1, count_nodes(tree) + 1)
                 if not isinstance(get_subtree(tree, i).data, str)]

    if not constants:
        return tree
    idx = random.choice(constants)
    old = get_subtree(tree, idx).data

    step_size = 0.1 * abs(old) + 0.01
    new_value = old + random.gauss(0, step_size)
    return replace_subtree(tree, idx, Node(new_value))

# Takes in two tree root nodes to crossover and swaps a subtree of each tree at random nodes in the trees
def crossover(tree_a, tree_b):
    idx_a = random.randint(1, count_nodes(tree_a))
    idx_b = random.randint(1, count_nodes(tree_b))
    subtree_a = get_subtree(tree_a, idx_a)
    subtree_b = get_subtree(tree_b, idx_b)

    crossover_a = replace_subtree(tree_a, idx_a, subtree_b)
    crossover_b = replace_subtree(tree_b, idx_b, subtree_a)

    a_depth = get_depth(crossover_a)
    b_depth = get_depth(crossover_b)

    if a_depth > MAX_DEPTH > b_depth:
        return tree_a, crossover_b
    elif b_depth > MAX_DEPTH > a_depth:
        return crossover_a, tree_b
    elif b_depth > MAX_DEPTH and a_depth > MAX_DEPTH:
        return tree_a, tree_b

    return crossover_a, crossover_b


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.right) + count_nodes(node.left)

def get_depth(node):
    if node is None:
        return 0
    return 1 + max(get_depth(node.right), get_depth(node.left))

def get_subtree(node, node_num):
    if node_num == 1:
        return node

    left_size = count_nodes(node.left)
    if node_num <= left_size + 1:
        return get_subtree(node.left, node_num - 1)
    return get_subtree(node.right, node_num - 1 - left_size)

def replace_subtree(node, node_num, subtree):
    if node_num == 1:
        return subtree

    left_size = count_nodes(node.left)
    if node_num <= left_size + 1:
        return Node(
            node.data,
            replace_subtree(node.left, node_num - 1, subtree),
            node.right
        )
    return Node(
        node.data,
        node.left,
        replace_subtree(node.right, node_num - 1 - left_size, subtree)
    )

def evaluate(node, val):
    if node.left is None and node.right is None:
        if isinstance(node.data, str):
            return val[node.data] if isinstance(val, dict) else val
        return node.data
    if node.data == '+':
        return evaluate(node.left, val) + evaluate(node.right, val)
    if node.data == '-':
        return evaluate(node.left, val) - evaluate(node.right, val)
    if node.data == '*':
        return evaluate(node.left, val) * evaluate(node.right, val)
    if node.data == '/':
        right = evaluate(node.right, val)
        right = np.where(np.abs(right) < .000000001, 1, right) # protects against division by 0 and too small denoms
        left = evaluate(node.left, val)
        return left / right

def to_string(node):
    if node.left is None and node.right is None:
        return str(node.data)
    return "(" + to_string(node.left) + str(node.data) + to_string(node.right) + ")"