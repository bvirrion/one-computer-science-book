"""catalan.py: the number of search-tree shapes with n nodes, by building the trees
of all insertion orders, and by the recurrence C(n) = sum C(i) C(n - 1 - i)."""

from itertools import permutations


def insert(t, k):
    if t is None:
        return (k, None, None)
    key, left, right = t
    if k < key:
        return (key, insert(left, k), right)
    return (key, left, insert(right, k))


def shape(t):
    return None if t is None else (shape(t[1]), shape(t[2]))


def shapes_by_program(n):
    seen = set()
    for order in permutations(range(n)):
        t = None
        for k in order:
            t = insert(t, k)
        seen.add(shape(t))
    return len(seen)


def shapes_by_recurrence(n):
    c = [1]
    for m in range(1, n + 1):
        c.append(sum(c[i] * c[m - 1 - i] for i in range(m)))
    return c[n]
