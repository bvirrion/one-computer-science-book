"""link_state.py: every router knows the whole map and runs Dijkstra from itself."""
import heapq


def dijkstra(graph, source):
    """Distance and first hop from source to every reachable router."""
    dist, first = {source: 0}, {source: source}
    heap, done = [(0, source)], set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, c in sorted(graph[u].items()):
            if v not in dist or d + c < dist[v]:
                dist[v] = d + c
                first[v] = v if u == source else first[u]   # the way out of source
                heapq.heappush(heap, (dist[v], v))
    return dist, first


def tables(graph):
    """What link state computes: one shortest-path tree per router."""
    return {u: dijkstra(graph, u) for u in graph}
