"""exo_visited.py: exercise 5, Kruskal with a visited flag in place of union--find."""

from mst_town import town


def kruskal_visited(vertices, edges):
    visited, tree = set(), []
    for w, u, v in sorted(edges):
        if u not in visited or v not in visited:  # "no cycle if an end is new"
            visited |= {u, v}
            tree.append((w, u, v))
    return tree


if __name__ == "__main__":
    vertices, edges = town()
    tree = kruskal_visited(vertices, edges)
    print(f"{len(tree)} roads kept for {len(vertices)} places")
