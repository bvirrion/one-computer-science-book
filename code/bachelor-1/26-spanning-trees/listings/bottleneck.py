"""bottleneck.py: the minimax road between two places (the smallest possible longest
road on a route) read from the minimum spanning tree, against a direct search."""

import heapq
from collections import Counter

from kruskal import kruskal
from mst_town import names, town


def tree_path_max(tree, a, b):
    """The longest edge on the path from a to b in the tree."""
    adj = {}
    for w, u, v in tree:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    stack, best = [(a, 0)], {a: 0}
    while stack:
        u, m = stack.pop()
        for v, w in adj.get(u, []):
            if v not in best:
                best[v] = max(m, w)
                stack.append((v, best[v]))
    return best[b]


def minimax(vertices, edges, a):
    """Dijkstra's algorithm with max in place of +: the smallest possible longest edge
    on a path from a to each vertex."""
    adj = {v: [] for v in vertices}
    for w, u, v in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    best, heap, done = {a: 0}, [(0, a)], set()
    while heap:
        m, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in adj[u]:
            if max(m, w) < best.get(v, float("inf")):
                best[v] = max(m, w)
                heapq.heappush(heap, (best[v], v))
    return best


if __name__ == "__main__":
    vertices, edges = town()
    tree, _ = kruskal(vertices, edges)
    name, direct = names(), minimax(vertices, edges, 1)
    same = all(tree_path_max(tree, 1, b) == direct[b] for b in vertices)
    print(f"from {name[1]}: tree answers = direct search for all 30 places: {same}")
    print(f"to the {name[8]}: no route avoids a road of {direct[8]} m")
    for k in (2, 3, 4, 5):  # remove the k - 1 longest tree edges: k clusters
        _, uf = kruskal(vertices, sorted(tree)[:1 - k])
        sizes = Counter(uf.find(v) for v in vertices).values()
        print(f"{k} clusters: sizes {sorted(sizes, reverse=True)}")
