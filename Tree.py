OPERATORS = [+, -, *, /]
MAX_DEPTH = 3

class Node:
	def __init__(self, data):
		self.data = data 
		self.left = None
		self.right = None

def randNode(isTerminal=False):
	if isTerminal: 
		x = random.randint(0,1)
	else: 
		x = random.randint(-1,1)
        if x == -1:
                return Node(OPERATORS[random.randint(0,3)])
	if x == 0:
		return Node("x")
	return Node(random.randint(-3,3))

def randTree():
	root = Node(OPERATORS[random.randint(0,3)])
	root.left = randNode()
	root.right = randNode()
	
	next_l = root.left
	next_r = root.right
	while(depth < 3):
		if next_l in OPERATORS:
			next_l.left = randNode()
			next_l.right = randNode()
		if next_r in OPERATORS:
			next_r.left = randNode()
			next_r.right = randNode()
		next_l = 


def helper(Node, depth=0):
	if depth => 2:
		Node.left = Node(random

	if Node in OPERATORS:
		Node
