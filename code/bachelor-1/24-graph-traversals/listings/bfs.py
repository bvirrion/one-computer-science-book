"""bfs.py: breadth-first search, the fewest roads from the Town Square to each place."""

from collections import deque

from graph import place_names, roads


def bfs(g, s):
    """(dist, parent): dist[v] is the number of edges of a shortest path from s to v."""
    dist, parent = {s: 0}, {s: None}
    queue = deque([s])
    while queue:
        u = queue.popleft()  # vertices leave in the order of their distance
        for v in g.adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)
    return dist, parent


def path(parent, v):
    out = []
    while v is not None:
        out.append(v)
        v = parent[v]
    return out[::-1]


def main():
    g, names = roads(), place_names()
    dist, parent = bfs(g, 1)
    for d in range(max(dist.values()) + 1):
        layer = sorted(v for v in dist if dist[v] == d)
        print(f"distance {d}: {len(layer):2} places", layer)
    far = max(dist, key=lambda v: (dist[v], -v))
    route = path(parent, far)
    print(f"farthest: {names[far]}, by")
    print("  " + " -> ".join(names[v] for v in route[:4]) + " ->")
    print("  " + " -> ".join(names[v] for v in route[4:]))


if __name__ == "__main__":
    main()
