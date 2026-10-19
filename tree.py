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

def generate_trees(num):
    trees = []
    for i in range(num):
        trees.append(rand_tree())
    return trees

def mutate(tree):
    idx = random.randint(1, count_nodes(tree))
    if random.randint(-1, 1) == -1:
        return replace_subtree(tree, idx, rand_tree())
    else:
        return replace_subtree(tree, idx, rand_leaf())

# Takes in two tree root nodes to crossover and swaps a subtree of each tree at random nodes in the trees
def crossover(tree_a, tree_b):
    idx_a = random.randint(1, count_nodes(tree_a))
    idx_b = random.randint(1, count_nodes(tree_b))
    subtree_a = get_subtree(tree_a, idx_a)
    subtree_b = get_subtree(tree_b, idx_b)

    crossover_a = replace_subtree(tree_a, idx_a, subtree_b)
    crossover_b = replace_subtree(tree_b, idx_b, subtree_a)
    return crossover_a, crossover_b


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.right) + count_nodes(node.left)

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