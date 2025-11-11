class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Global variables
tokens = []
index = 0
temp_count = 1
instructions = []


def get_token():
    """Return the current token without consuming it."""
    global index
    if index < len(tokens):
        return tokens[index]
    return None


def match(expected):
    """Consume a token if it matches the expected symbol."""
    global index
    if get_token() == expected:
        index += 1
    else:
        raise Exception(f"Syntax Error: Expected '{expected}', got '{get_token()}'")


# Grammar:
# E -> T { (+|-) T }
# T -> F { (*|/) F }
# F -> (E) | id

def parse_F():
    tok = get_token()
    if tok == '(':
        match('(')
        node = parse_E()
        match(')')
        return node
    elif tok.isalnum():
        match(tok)
        return Node(tok)
    else:
        raise Exception(f"Unexpected token {tok}")


def parse_T():
    node = parse_F()
    while True:
        tok = get_token()
        if tok == '*':
            match('*')
            node = Node('*', node, parse_F())
        elif tok == '/':
            match('/')
            node = Node('/', node, parse_F())
        else:
            break
    return node


def parse_E():
    node = parse_T()
    while True:
        tok = get_token()
        if tok == '+':
            match('+')
            node = Node('+', node, parse_T())
        elif tok == '-':
            match('-')
            node = Node('-', node, parse_T())
        else:
            break
    return node


def generate_code(node):
    """Generate three-address code from the AST."""
    global temp_count, instructions

    # Leaf node (identifier or number)
    if node.left is None and node.right is None:
        return node.value

    left = generate_code(node.left)
    right = generate_code(node.right)

    temp = f"T{temp_count}"
    temp_count += 1

    if node.value == '+':
        instructions.append(f"ADD {left}, {right} -> {temp}")
    elif node.value == '-':
        instructions.append(f"SUB {left}, {right} -> {temp}")
    elif node.value == '*':
        instructions.append(f"MUL {left}, {right} -> {temp}")
    elif node.value == '/':
        instructions.append(f"DIV {left}, {right} -> {temp}")
    else:
        raise Exception(f"Unknown operator {node.value}")

    return temp


def postorder(node):
    """Postorder traversal of AST."""
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.value, end=" ")


# --- MAIN PROGRAM ---
expr = input("Enter arithmetic expression (e.g., a+b*c): ").replace(" ", "")
tokens = [ch for ch in expr] + ['$']
index = 0

# Parse expression
root = parse_E()

print("\nABSTRACT SYNTAX TREE GENERATED SUCCESSFULLY!")
print("(Postorder Traversal):")
postorder(root)

print("\n\nGENERATED MACHINE CODE (Three-Address Instructions):")
generate_code(root)
for ins in instructions:
    print(ins)
