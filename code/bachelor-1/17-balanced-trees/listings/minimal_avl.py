"""minimal_avl.py: the AVL trees of height h with the fewest nodes, built, counted."""

import math


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def minimal(h):
    """A minimal AVL tree of height h, as nested (left, right) pairs; None is empty."""
    if h < 0:
        return None
    if h == 0:
        return (None, None)
    return (minimal(h - 1), minimal(h - 2))


def size(t):
    return 0 if t is None else 1 + size(t[0]) + size(t[1])


def height(t):
    return -1 if t is None else 1 + max(height(t[0]), height(t[1]))


def is_avl(t):
    return t is None or (abs(height(t[0]) - height(t[1])) <= 1
                         and is_avl(t[0]) and is_avl(t[1]))


def max_height(n):
    """The largest height of an AVL tree with n nodes: the largest h with N(h) <= n."""
    h = 0
    while size(minimal(h + 1)) <= n:
        h += 1
    return h


def main():
    print(f"{'h':>2} {'N(h)':>6} {'F(h+3)-1':>9} {'1.44 lg(N+2)':>13}")
    for h in [*range(11), 15, 20]:
        t = minimal(h)
        n = size(t)
        assert height(t) == h and is_avl(t)
        print(f"{h:2} {n:6} {fib(h + 3) - 1:9} {1.4405 * math.log2(n + 2):13.2f}")
    print("largest height of an AVL tree with 80 nodes:", max_height(80))


if __name__ == "__main__":
    main()
