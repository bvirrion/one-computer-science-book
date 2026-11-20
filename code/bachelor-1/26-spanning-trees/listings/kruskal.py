"""kruskal.py: a minimum spanning tree by Kruskal's algorithm: the roads by increasing
length, each kept unless it closes a cycle."""

from mst_town import names, town
from union_find import UnionFind


def kruskal(vertices, edges):
    """(tree, uf): tree is the list of edges kept, as (w, u, v)."""
    uf, tree = UnionFind(vertices), []
    for w, u, v in sorted(edges):
        if uf.union(u, v):  # u and v were in different trees: no cycle
            tree.append((w, u, v))
            if len(tree) == len(vertices) - 1:
                break
    return tree, uf


def main():
    vertices, edges = town()
    tree, uf = kruskal(vertices, edges)
    name = names()
    print(f"{len(tree)} roads, {sum(w for w, _, _ in tree)} m of fibre;"
          f" {uf.steps} parent steps in the finds")
    print("shortest three:")
    print("  " + "; ".join(f"{name[u]}-{name[v]} {w}" for w, u, v in tree[:3]))
    w, u, v = tree[-1]
    print(f"longest: {name[u]}-{name[v]} {w}")


if __name__ == "__main__":
    main()
