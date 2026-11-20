"""prim.py: a minimum spanning tree by Prim's algorithm: one tree grown from a vertex,
always by the lightest edge leaving it, found with a heap."""

import heapq

from mst_town import town


def prim(vertices, edges, start):
    adj = {v: [] for v in vertices}
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    inside, tree, pops = {start}, [], 0
    heap = [(w, start, v) for w, v in adj[start]]
    heapq.heapify(heap)
    while heap and len(inside) < len(vertices):
        w, u, v = heapq.heappop(heap)
        pops += 1
        if v in inside:  # both ends inside: the edge no longer crosses the cut
            continue
        inside.add(v)
        tree.append((w, u, v))
        for x in adj[v]:
            if x[1] not in inside:
                heapq.heappush(heap, (x[0], v, x[1]))
    return tree, pops


if __name__ == "__main__":
    vertices, edges = town()
    for start in (1, 8):
        tree, pops = prim(vertices, edges, start)
        print(f"from {start}: {len(tree)} roads, {sum(w for w, _, _ in tree)} m,"
              f" {pops} pops")
