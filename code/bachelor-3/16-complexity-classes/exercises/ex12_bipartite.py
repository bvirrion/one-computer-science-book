"""ex12_bipartite.py -- exercise 12: is an undirected graph 2-colourable, with no list
and no set, only a few vertex numbers at a time? A graph is 2-colourable if and only if
no vertex v reaches (v, odd) in the parity graph, whose vertex (x, p) records the
parity p of a walk's length. Reachability there is Savitch's midpoint recursion."""
import math


def adjacent(edges, x, y):
    return (x, y) in edges or (y, x) in edges


def reach(edges, n, x, p, y, q, k):
    """A walk from x to y of length at most 2^k whose length has parity p xor q."""
    if k == 0:
        return (x, p) == (y, q) or (adjacent(edges, x, y) and p != q)
    return any(reach(edges, n, x, p, w, r, k - 1) and reach(edges, n, w, r, y, q, k - 1)
               for w in range(n) for r in (0, 1))


def two_colourable(n, edges):
    k = max(1, math.ceil(math.log2(2 * n)))
    return not any(reach(edges, n, v, 0, v, 1, k) for v in range(n))
