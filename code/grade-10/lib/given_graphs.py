"""Graph functions given to grade 10 as black boxes; grade 12 writes them."""
from collections import deque


def distances(g, start):
    """Return a dict: vertex -> edges of a shortest path from start (reachable ones)."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for w in sorted(g[v]):
            if w not in dist:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def components(g):
    """Return the list of connected components (sets of vertices), largest first."""
    seen, parts = set(), []
    for v in sorted(g):
        if v not in seen:
            part = set(distances(g, v))
            seen |= part
            parts.append(part)
    return sorted(parts, key=lambda p: (-len(p), min(p)))
