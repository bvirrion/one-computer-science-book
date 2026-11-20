"""inductive.py: binary trees as an inductively defined set."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    left: "Node | None"  # None is the empty tree
    key: int
    right: "Node | None"


def size(t):
    return 0 if t is None else 1 + size(t.left) + size(t.right)


def height(t):
    return -1 if t is None else 1 + max(height(t.left), height(t.right))


def leaves(t):
    if t is None:
        return 0
    if t.left is None and t.right is None:
        return 1
    return leaves(t.left) + leaves(t.right)


def shapes(h):
    """All binary trees of height at most h, keys 0: rule 1 gives the empty
    tree, rule 2 builds a node from two trees already built."""
    if h < 0:
        return [None]
    smaller = shapes(h - 1)
    return [None] + [Node(a, 0, b) for a in smaller for b in smaller]


if __name__ == "__main__":
    t = Node(Node(None, 2, None), 5, Node(Node(None, 7, None), 9, None))
    print("size", size(t), "height", height(t), "leaves", leaves(t))
    print("empty tree: size", size(None), "height", height(None))
    for h in range(-1, 4):
        trees = shapes(h)
        print(f"height <= {h:2d}: {len(trees):3d} trees, largest size"
              f" {max(map(size, trees)):2d}, 2^(h+1) - 1 = {2 ** (h + 1) - 1:2d}")
