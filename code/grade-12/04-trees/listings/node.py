"""Binary trees: None is the empty tree, a Node has a value and two subtrees."""


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def size(t):
    if t is None:
        return 0
    return 1 + size(t.left) + size(t.right)


def height(t):
    if t is None:
        return -1                  # so that a single node has height 0
    return 1 + max(height(t.left), height(t.right))


def leaves(t):
    if t is None:
        return 0
    if t.left is None and t.right is None:
        return 1
    return leaves(t.left) + leaves(t.right)
