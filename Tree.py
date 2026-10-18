import random
from collections import deque

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

def generate_trees(num):
    trees = []
    for i in range(num):
        trees.append(rand_tree())
    return trees

def mutate(node):
    if random.randint(-1, 1) == -1:
        node.left = rand_tree()
    else:
        node.left = rand_leaf()

    if random.randint(-1, 1) == -1:
        node.right = rand_tree()
    else:
        node.right = rand_leaf()

# Takes in two tree root nodes to crossover and swaps a subtree of each tree at random nodes in the trees
def crossover(tree_a, tree_b):
    node_a, side_a = get_node(tree_a, random.randint(1, count_nodes(tree_a)))
    node_b, side_b = get_node(tree_b, random.randint(1, count_nodes(tree_b)))

    a = getattr(node_a, side_a)
    b = getattr(node_b, side_b)

    setattr(node_a, side_a, b)
    setattr(node_b, side_b, a)


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.right) + count_nodes(node.left)

def get_node(root, node_num):
    node = parent = None
    queue = deque()
    queue.append((root, None))

    for _ in range(node_num):
        node, parent = queue.popleft()
        if node.left is not None:
            queue.append((node.left, node))
        if node.right is not None:
            queue.append((node.right, node))
    side = 'left' if node_num % 2 == 0 else 'right'
    return parent, side

