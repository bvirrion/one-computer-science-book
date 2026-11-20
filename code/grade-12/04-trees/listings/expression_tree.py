from node import Node

OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}


def evaluate(t):                       # postorder: both operands, then the operator
    if t.left is None:
        return t.value                 # a leaf is a number
    return OPS[t.value](evaluate(t.left), evaluate(t.right))


def infix(t):                          # inorder, with brackets around each operation
    if t.left is None:
        return str(t.value)
    return f"({infix(t.left)} {t.value} {infix(t.right)})"


def postfix(t):
    if t.left is None:
        return str(t.value)
    return f"{postfix(t.left)} {postfix(t.right)} {t.value}"


e = Node("*", Node("+", Node(3), Node(4)), Node("-", Node(5), Node(2)))
print(infix(e), "=", evaluate(e))
print("postfix:", postfix(e))
