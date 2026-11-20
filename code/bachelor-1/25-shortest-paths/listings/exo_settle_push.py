"""exo_settle_push.py: exercise 5, Dijkstra fixing a vertex's distance when pushed."""

import heapq


def dijkstra_push(adj, s):
    dist, heap = {s: 0}, [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            if v not in dist:  # fixed at the first discovery
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


if __name__ == "__main__":
    print(dijkstra_push({"s": [("a", 5), ("b", 1)], "b": [("a", 1)], "a": []}, "s"))
