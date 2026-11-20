"""lcrs.py: a tree of any arity as a binary tree, left child and right sibling."""

from dataclasses import dataclass, field

from inductive import Node


@dataclass
class Tree:  # a node of any arity: a key and a list of children
    key: int
    children: list = field(default_factory=list)


def to_binary(t, siblings=()):
    """t and its younger siblings as one binary tree: left = first child of t,
    right = the next sibling of t."""
    first = to_binary(t.children[0], t.children[1:]) if t.children else None
    nxt = to_binary(siblings[0], siblings[1:]) if siblings else None
    return Node(first, t.key, nxt)


def from_binary(b):
    """The inverse: the list of trees that b and its right spine encode."""
    trees = []
    while b is not None:
        trees.append(Tree(b.key, from_binary(b.left)))
        b = b.right
    return trees


def show(b):
    return "." if b is None else f"({show(b.left)} {b.key} {show(b.right)})"


if __name__ == "__main__":
    t = Tree(1, [Tree(2), Tree(3, [Tree(6), Tree(7)]), Tree(4), Tree(5, [Tree(8)])])
    b = to_binary(t)
    print("binary tree:", show(b))
    print("back again equal:", from_binary(b) == [t])
