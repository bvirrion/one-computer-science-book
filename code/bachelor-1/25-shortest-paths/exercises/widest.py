"""widest.py: the widest path, whose narrowest arc is as wide as possible, by a variant
of Dijkstra's algorithm that keeps the largest bottleneck."""

import heapq


def widest(adj, s):
    width = {v: 0 for v in adj}
    width[s] = float("inf")
    heap, done = [(-width[s], s)], set()
    while heap:
        _, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, c in adj[u]:
            b = min(width[u], c)  # the bottleneck of the path through u
            if b > width[v]:
                width[v] = b
                heapq.heappush(heap, (-b, v))
    return width
