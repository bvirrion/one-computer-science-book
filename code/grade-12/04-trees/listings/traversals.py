from collections import deque

from node import Node


def preorder(t):                      # the node, then its left, then its right
    return [] if t is None else [t.value] + preorder(t.left) + preorder(t.right)


def inorder(t):                       # left, the node, right
    return [] if t is None else inorder(t.left) + [t.value] + inorder(t.right)


def postorder(t):                     # left, right, the node last
    return [] if t is None else postorder(t.left) + postorder(t.right) + [t.value]


def breadth_first(t):                 # level by level, with a queue
    out, line = [], deque([t] if t is not None else [])
    while line:
        node = line.popleft()
        out.append(node.value)
        for child in (node.left, node.right):
            if child is not None:
                line.append(child)
    return out


if __name__ == "__main__":
    t = Node("A", Node("B", Node("D"), Node("E", Node("G"))),
             Node("C", None, Node("F")))
    for order in [preorder, inorder, postorder, breadth_first]:
        print(f"{order.__name__:13}", " ".join(order(t)))
