"""ex6_one_tree.py -- the 1-tree lower bound for the travelling salesman problem: a
minimum spanning tree of every place but the first, plus the two shortest edges from
the first. A tour is such a structure, so the bound never exceeds the optimum."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from tsp import dist, minimum_spanning_tree  # noqa: E402


def one_tree_bound(points):
    rest = points[1:]
    children = minimum_spanning_tree(rest)
    tree = sum(dist(rest[u], rest[v]) for u in children for v in children[u])
    two = sorted(dist(points[0], q) for q in rest)[:2]
    return tree + sum(two)
