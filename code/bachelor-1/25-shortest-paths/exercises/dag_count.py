"""dag_count.py: the distance from s and the number of shortest paths to every vertex of
a weighted directed acyclic graph, in topological order."""

INF = float("inf")


def count_paths(adj, order, s):
    """order: a topological order of the vertices."""
    dist, ways = {v: INF for v in adj}, {v: 0 for v in adj}
    dist[s], ways[s] = 0, 1
    for u in order:
        if dist[u] == INF:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v], ways[v] = dist[u] + w, ways[u]
            elif dist[u] + w == dist[v]:
                ways[v] += ways[u]
    return dist, ways
