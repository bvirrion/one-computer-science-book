"""Exercises of the chapter on trees."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from node import Node  # noqa: E402


def count_at_depth(t, d):                      # exercise 5
    if t is None:
        return 0
    if d == 0:
        return 1
    return count_at_depth(t.left, d - 1) + count_at_depth(t.right, d - 1)


def bst_min(t):                                # exercise 7
    if t is None:
        raise ValueError("an empty tree has no smallest key")
    while t.left is not None:
        t = t.left
    return t.value


def insert_broken(t, key):                     # exercise 10: the staged fault
    if t is None:
        return Node(key)
    if key < t.value:
        insert_broken(t.left, key)             # the new subtree is thrown away
    else:
        insert_broken(t.right, key)
    return t


def insert_fixed(t, key):
    if t is None:
        return Node(key)
    if key < t.value:
        t.left = insert_fixed(t.left, key)
    elif key > t.value:
        t.right = insert_fixed(t.right, key)
    return t


def is_bst_wrong(t):                           # exercise 11: checks only the children
    if t is None:
        return True
    if t.left is not None and t.left.value >= t.value:
        return False
    if t.right is not None and t.right.value <= t.value:
        return False
    return is_bst_wrong(t.left) and is_bst_wrong(t.right)


def is_bst(t, low=None, high=None):            # exercise 11: every key in its interval
    if t is None:
        return True
    if (low is not None and t.value <= low) or (high is not None and t.value >= high):
        return False
    return is_bst(t.left, low, t.value) and is_bst(t.right, t.value, high)


def rebuild(pre, ino):                         # exercise 14: distinct values
    if not pre:
        return None
    root = pre[0]
    k = ino.index(root)                        # k values on the left
    return Node(root, rebuild(pre[1:k + 1], ino[:k]), rebuild(pre[k + 1:], ino[k + 1:]))


def count_shapes(n):                           # exercise 15
    if n == 0:
        return 1
    return sum(count_shapes(k) * count_shapes(n - 1 - k) for k in range(n))


if __name__ == "__main__":
    t = Node(5, Node(3, None, Node(6)), Node(8))
    print(is_bst_wrong(t), is_bst(t), [count_shapes(n) for n in range(6)])
