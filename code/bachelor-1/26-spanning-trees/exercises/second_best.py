"""second_best.py: the weight of a second-best spanning tree: swap one edge of a minimum
spanning tree for one outside it, every way, and keep the lightest spanning result."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from kruskal import kruskal  # noqa: E402
from union_find import UnionFind  # noqa: E402


def second_best(vertices, edges):
    tree, _ = kruskal(vertices, edges)
    others = [e for e in edges if e not in tree]
    best = None
    for out in tree:
        for e in others:
            candidate = [t for t in tree if t != out] + [e]
            uf = UnionFind(vertices)
            if all(uf.union(u, v) for _, u, v in candidate):  # still a spanning tree
                w = sum(x[0] for x in candidate)
                best = w if best is None else min(best, w)
    return best
