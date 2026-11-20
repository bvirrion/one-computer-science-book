"""rank_height.py: union by rank without path compression: the tallest tree after random
unions, against log2 n."""

import math
import random

from union_find import UnionFind


def height(uf, x):
    h = 0
    while uf.parent[x] != x:
        x, h = uf.parent[x], h + 1
    return h


def unions_only(uf, x, y):
    """union by rank with finds that do not compress."""
    rx, ry = x, y
    while uf.parent[rx] != rx:
        rx = uf.parent[rx]
    while uf.parent[ry] != ry:
        ry = uf.parent[ry]
    if rx != ry:
        if uf.rank[rx] < uf.rank[ry]:
            rx, ry = ry, rx
        uf.parent[ry] = rx
        uf.rank[rx] += uf.rank[rx] == uf.rank[ry]


def pairing(n):
    """Merge trees of equal rank, two by two: the worst case."""
    uf, size = UnionFind(range(n)), 1
    while size < n:
        for i in range(0, n, 2 * size):
            unions_only(uf, i, i + size)
        size *= 2
    return uf


if __name__ == "__main__":
    rng = random.Random(26)
    for n in (16, 256, 4096, 65536):
        uf = UnionFind(range(n))
        for _ in range(4 * n):
            unions_only(uf, rng.randrange(n), rng.randrange(n))
        tallest = max(height(uf, x) for x in range(n))
        tree = pairing(n)
        worst = max(height(tree, x) for x in range(n))
        print(f"n = {n:5}: random unions {tallest:2}, pairing {worst:2},"
              f" log2 n = {math.log2(n):2.0f}")
