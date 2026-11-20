"""count_trees.py: every spanning tree of a small piece of the town, by brute force:
the places within two roads of the Town Square."""

from itertools import combinations

from kruskal import kruskal
from mst_town import town
from union_find import UnionFind


def spanning_trees(vertices, edges):
    """Every set of n - 1 edges without a cycle: exactly the spanning trees."""
    for chosen in combinations(edges, len(vertices) - 1):
        uf = UnionFind(vertices)
        if all(uf.union(u, v) for _, u, v in chosen):
            yield chosen


if __name__ == "__main__":
    vertices, edges = town()
    near = {1}
    for _ in range(2):
        step = {b for _, a, b in edges if a in near}
        near |= step | {a for _, a, b in edges if b in near}
    piece = [e for e in edges if e[1] in near and e[2] in near]
    trees = list(spanning_trees(sorted(near), piece))
    lightest = min(sum(w for w, _, _ in t) for t in trees)
    tree, _ = kruskal(sorted(near), piece)
    sets = sum(1 for _ in combinations(piece, len(near) - 1))
    print(f"{len(near)} places, {len(piece)} roads: {len(trees)} spanning trees"
          f" among {sets} sets of {len(near) - 1} roads")
    print(f"lightest by brute force {lightest} m,"
          f" by Kruskal {sum(w for w, _, _ in tree)} m")
