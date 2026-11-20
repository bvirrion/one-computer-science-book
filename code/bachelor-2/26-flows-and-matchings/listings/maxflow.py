"""maxflow.py: flow networks, residual capacities, Ford-Fulkerson with a choice of
augmenting paths, and the minimum cut read from the final residual network."""
from collections import deque


class Network:
    def __init__(self):
        self.cap = {}  # (u, v) -> capacity; a missing pair has capacity 0
        self.adj = {}  # u -> the vertices v with (u, v) or (v, u) an edge

    def add_edge(self, u, v, c):
        self.cap[(u, v)] = self.cap.get((u, v), 0) + c
        for a, b in [(u, v), (v, u)]:
            self.adj.setdefault(a, [])
            if b not in self.adj[a]:
                self.adj[a].append(b)  # residual edges go both ways

    def residual(self, flow, u, v):
        """What can still be pushed from u to v: unused capacity, plus flow v -> u
        that can be cancelled."""
        return self.cap.get((u, v), 0) - flow.get((u, v), 0) + flow.get((v, u), 0)


def shortest_path(net, flow, s, t):
    """A shortest augmenting path by breadth-first search, as a list of vertices."""
    parent, queue = {s: None}, deque([s])
    while queue:
        u = queue.popleft()
        for v in net.adj.get(u, []):
            if v not in parent and net.residual(flow, u, v) > 0:
                parent[v] = u
                if v == t:
                    path = [t]
                    while path[-1] != s:
                        path.append(parent[path[-1]])
                    return path[::-1]
                queue.append(v)
    return None


def augment(net, flow, path):
    """Push the bottleneck along path, cancelling reverse flow first."""
    pairs = list(zip(path, path[1:]))
    delta = min(net.residual(flow, u, v) for u, v in pairs)
    for u, v in pairs:
        back = min(delta, flow.get((v, u), 0))  # cancel flow v -> u first
        flow[(v, u)] = flow.get((v, u), 0) - back
        flow[(u, v)] = flow.get((u, v), 0) + delta - back
    return delta


def max_flow(net, s, t, find=shortest_path, log=None):
    """Ford-Fulkerson; with shortest paths, Edmonds-Karp. Returns (value, flow)."""
    flow, value = {}, 0
    while (path := find(net, flow, s, t)) is not None:
        delta = augment(net, flow, path)
        value += delta
        if log is not None:
            log.append((path, delta))
    return value, {e: f for e, f in flow.items() if f > 0}


def min_cut(net, flow, s):
    """The vertices reachable from s in the residual network; the edges leaving them."""
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for v in net.adj.get(u, []):
            if v not in seen and net.residual(flow, u, v) > 0:
                seen.add(v)
                stack.append(v)
    edges = [(u, v) for (u, v), c in net.cap.items()
             if u in seen and v not in seen and c > 0]
    return seen, sorted(edges, key=str)
