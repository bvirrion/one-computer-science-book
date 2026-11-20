from collections import deque

from representations import G


def bfs(g, start):
    """Distances in edges from start, and each vertex's parent on a shortest path."""
    dist, parent = {start: 0}, {start: None}
    line = deque([start])
    while line:
        v = line.popleft()
        for w in g[v]:
            if w not in dist:                # first time seen: by a shortest path
                dist[w] = dist[v] + 1
                parent[w] = v
                line.append(w)
    return dist, parent


def path_to(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


if __name__ == "__main__":
    dist, parent = bfs(G, "A")
    print("distances:", dist)
    print("parents:  ", parent)
    print("a shortest path to F:", path_to(parent, "F"))
