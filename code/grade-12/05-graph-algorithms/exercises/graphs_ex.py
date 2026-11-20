"""Exercises of the chapter on graph algorithms."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))


def count_edges(adj):                              # exercise 5: undirected graph
    return sum(len(ns) for ns in adj.values()) // 2


def all_paths_calls(g, v, on_path=None):           # exercise 6: the staged fault
    """A search that marks only the current path: it explores every path."""
    on_path = on_path or set()
    on_path.add(v)
    calls = 1
    for w in g[v]:
        if w not in on_path:
            calls += all_paths_calls(g, w, on_path)
    on_path.remove(v)                              # un-marked on the way back
    return calls


def has_path(g, a, b):                             # exercise 7
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return True
        for w in g[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return False


def dijkstra_last(g, source):                      # exercise 9: the staged fault
    dist, done = {source: 0}, set()
    while True:
        waiting = [v for v in dist if v not in done]
        if not waiting:
            return dist
        u = waiting[-1]                            # the last added, not the closest
        done.add(u)
        for v, w in g[u].items():
            if v not in done and (v not in dist or dist[u] + w < dist[v]):
                dist[v] = dist[u] + w


def bfs_layers(g, s):                              # exercise 11
    layers, seen = [[s]], {s}
    while True:
        nxt = []
        for v in layers[-1]:
            for w in g[v]:
                if w not in seen:
                    seen.add(w)
                    nxt.append(w)
        if not nxt:
            return layers
        layers.append(nxt)


def topological_order(g):                          # exercise 14
    """An order where every edge goes forwards; ValueError if there is a cycle."""
    state, order = {v: 0 for v in g}, []           # 0 new, 1 in progress, 2 done

    def explore(v):
        state[v] = 1
        for w in g[v]:
            if state[w] == 1:
                raise ValueError("the graph has a cycle")
            if state[w] == 0:
                explore(w)
        state[v] = 2
        order.append(v)                            # after all its successors

    for v in g:
        if state[v] == 0:
            explore(v)
    return order[::-1]


def count_shortest(g, dist, s, t):               # problem, question 12
    ways = {s: 1}
    for v in sorted(dist, key=dist.get):
        if v != s:
            ways[v] = sum(ways[u] for u in g[v] if dist.get(u) == dist[v] - 1)
    return ways[t]


def grid(n):
    return {(r, c): [(r + dr, c + dc) for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1))
                     if 0 <= r + dr < n and 0 <= c + dc < n]
            for r in range(n) for c in range(n)}


if __name__ == "__main__":
    from dijkstra import W
    print([all_paths_calls(grid(n), (0, 0)) for n in (2, 3, 4)])
    print(dijkstra_last(W, "S"))
    print(topological_order({"maths": ["cs"], "cs": ["engineering"],
                             "engineering": []}))
