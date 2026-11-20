"""negative_cycle.py: a cycle of negative weight, as a list of vertices, or None."""


def negative_cycle(adj):
    """Bellman--Ford from a virtual source with an arc of weight 0 to every vertex."""
    dist, parent = {v: 0 for v in adj}, {v: None for v in adj}
    last = None
    for _ in range(len(adj)):
        last = None
        for u in adj:
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v], parent[v] = dist[u] + w, u
                    last = v
        if last is None:
            return None
    for _ in range(len(adj)):  # walk back n steps: we are now on the cycle
        last = parent[last]
    cycle, v = [last], parent[last]
    while v != last:
        cycle.append(v)
        v = parent[v]
    return cycle[::-1]
