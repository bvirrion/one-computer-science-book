"""Binary search trees: smaller keys on the left, larger on the right."""
from node import Node


def insert(t, key):
    """Return the tree t with key added; a key already there is not added again."""
    new = Node(key)
    if t is None:
        return new
    node = t
    while True:                         # a loop, not recursion: trees can be deep
        if key == node.value:
            return t
        side = "left" if key < node.value else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, new)
            return t
        node = child


def search(t, key):
    """Return the number of nodes visited to find key, or None if absent."""
    visited = 0
    while t is not None:
        visited += 1
        if key == t.value:
            return visited
        t = t.left if key < t.value else t.right
    return None


def build(keys):
    t = None
    for k in keys:
        t = insert(t, k)
    return t
