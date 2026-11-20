"""count_paths.py: the number of shortest paths from s to every vertex, by BFS."""

from collections import deque


def count_shortest(adj, s):
    dist, ways = {s: 0}, {s: 1}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v], ways[v] = dist[u] + 1, 0
                queue.append(v)
            if dist[v] == dist[u] + 1:  # u is a predecessor of v on a shortest path
                ways[v] += ways[u]
    return dist, ways
