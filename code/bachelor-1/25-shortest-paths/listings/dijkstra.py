"""dijkstra.py: shortest paths from one place with non-negative weights, a binary
heap and lazy deletion; the fastest and the shortest way to the Hospital."""

import heapq

from wgraph import names, roads

INF = float("inf")


def dijkstra(adj, s):
    """(dist, parent, pops): pops counts entries taken off the heap, stale or not."""
    dist, parent = {v: INF for v in adj}, {s: None}
    dist[s] = 0
    heap, settled, pops = [(0, s)], set(), 0
    while heap:
        d, u = heapq.heappop(heap)
        pops += 1
        if u in settled:  # a stale entry: u was settled with a smaller key
            continue
        settled.add(u)
        for v, w in adj[u]:
            if d + w < dist[v]:  # relax the arc u -> v
                dist[v], parent[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return dist, parent, pops


def path(parent, v):
    out = []
    while v is not None:
        out.append(v)
        v = parent[v]
    return out[::-1]


def main():
    name, seconds, metres = names(), roads("seconds"), roads("metres")
    for label, adj, other in (("fastest", seconds, metres),
                              ("shortest", metres, seconds)):
        dist, parent, pops = dijkstra(adj, 1)
        route = path(parent, 8)
        cost = dict(((u, v), w) for u in other for v, w in other[u])
        extra = sum(cost[a] for a in zip(route, route[1:]))
        m, s = (extra, dist[8]) if label == "fastest" else (dist[8], extra)
        print(f"{label}: {m} m in {s} s, {len(route) - 1} roads, {pops} pops")
        print("  via " + ", ".join(name[v] for v in route[1:-1]))


if __name__ == "__main__":
    main()
