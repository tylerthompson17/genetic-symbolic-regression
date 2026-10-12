import random

OPERATORS = ['+','-','/','*']
MAX_DEPTH = 3

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def rand_leaf():
    rand = random.randint(0, 1)
    if rand == 0:
        return Node(random.randint(-3, 3))
    return Node("x")

def rand_tree(depth = 0):
    rand = random.randint(-1, 1)
    if depth >= MAX_DEPTH or (depth > 0 and rand >= 0):
        return rand_leaf()
    return Node(
        random.choice(OPERATORS),
        rand_tree(depth + 1),
        rand_tree(depth + 1)
    )

def mutate(node):
    if random.randint(-1, 1) == -1:
        node.left = rand_tree()
    else:
        node.left = rand_leaf()

    if random.randint(-1, 1) == -1:
        node.right = rand_tree()
    else:
        node.right = rand_leaf()

# takes two parent nodes of two trees of the randomly selected nodes and which side it is
# on to perform crossover
def crossover(node_a, side_a, node_b, side_b):
    if side_a == 0:
        a = node_a.left
    else:
        a = node_a.right

    if side_b == 0:
        b = node_b.left
    else:
        b = node_b.right

    if side_a == 0:
        node_a.left = b
    else:
        node_a.right = b

    if side_b == 0:
        node_b.left = a
    else:
        node_b.right = a