"""exo_height0.py: exercise 6, a height that gives 0 to the empty tree."""

from inductive import Node, size


def height0(t):
    return 0 if t is None else 1 + max(height0(t.left), height0(t.right))


leaf = Node(None, 1, None)
for name, t in [("empty", None), ("leaf", leaf), ("three nodes", Node(leaf, 2, leaf))]:
    h = height0(t)
    print(f"{name:12} height0 {h}  size {size(t)}  size <= 2^(h+1) - 1: "
          f"{size(t) <= 2 ** (h + 1) - 1}  size >= h + 1: {size(t) >= h + 1}")
