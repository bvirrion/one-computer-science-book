"""boruvka.py: a minimum spanning tree by Boruvka's method: in each round, every tree
of the forest takes its lightest leaving edge; the number of trees at least halves."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from union_find import UnionFind  # noqa: E402


def boruvka(vertices, edges):
    """Distinct weights, or ties broken consistently, as by comparing the tuples."""
    uf, tree, rounds = UnionFind(vertices), [], 0
    while len(tree) < len(vertices) - 1:
        rounds += 1
        cheapest = {}
        for e in edges:
            ru, rv = uf.find(e[1]), uf.find(e[2])
            if ru != rv:
                for r in (ru, rv):
                    if r not in cheapest or e < cheapest[r]:
                        cheapest[r] = e
        if not cheapest:
            break  # the graph is not connected
        for e in set(cheapest.values()):
            if uf.union(e[1], e[2]):
                tree.append(e)
    return tree, rounds
