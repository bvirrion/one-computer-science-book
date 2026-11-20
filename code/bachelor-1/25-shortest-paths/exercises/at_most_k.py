"""at_most_k.py: the shortest paths that use at most k arcs (any weights)."""

INF = float("inf")


def at_most_k(adj, s, k):
    dist = {v: INF for v in adj}
    dist[s] = 0
    for _ in range(k):
        before = dict(dist)  # relax from the previous round only: one more arc
        for u in adj:
            for v, w in adj[u]:
                if before[u] + w < dist[v]:
                    dist[v] = before[u] + w
    return dist
