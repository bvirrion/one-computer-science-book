import heapq
import random

from hypothesis import given, settings
from hypothesis import strategies as st

from eight_puzzle import GOAL, manhattan, misplaced, scrambled, successors
from state_space import astar, bfs, iterative_deepening
from town_map import ROADS, straight


def dijkstra(adj, s):
    dist, heap = {s: 0}, [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist


@settings(max_examples=150, deadline=None)
@given(st.integers(0, 10**6))
def test_astar_equals_dijkstra_with_admissible_heuristics(seed):
    rng = random.Random(seed)
    n = rng.randrange(2, 12)
    xy = {v: (rng.randrange(100), rng.randrange(100)) for v in range(n)}
    adj = {}
    for _ in range(rng.randrange(1, 30)):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:  # a road is never shorter than the straight line
            d = ((xy[u][0] - xy[v][0]) ** 2 + (xy[u][1] - xy[v][1]) ** 2) ** 0.5
            adj.setdefault(u, []).append((v, d + rng.randrange(20)))
    dist = dijkstra(adj, 0)
    t = rng.randrange(n)

    def h(x):
        return ((xy[x][0] - xy[t][0]) ** 2 + (xy[x][1] - xy[t][1]) ** 2) ** 0.5

    path, cost, _ = astar(0, lambda x: x == t, lambda x: adj.get(x, []), h)
    if t in dist:
        assert abs(cost - dist[t]) < 1e-6
        length = sum(min(w for x, w in adj[u] if x == v) for u, v in zip(path, path[1:]))
        assert abs(length - cost) < 1e-6
    else:
        assert path is None


def test_town_heuristic_admissible_and_consistent():
    for u in ROADS:
        for v, d in ROADS[u]:
            assert straight(u, v) <= d
            for t in ROADS:
                assert straight(u, t) <= d + straight(v, t) + 1e-9


def test_eight_puzzle_searches_agree():
    rng = random.Random(1)
    for walk in [5, 10, 15, 25]:
        start = scrambled(walk, rng)
        p, _ = bfs(start, lambda s: s == GOAL, successors)
        q, _ = iterative_deepening(start, lambda s: s == GOAL, successors)
        for h in (misplaced, manhattan):
            r, c, _ = astar(start, lambda s: s == GOAL, successors, h)
            assert c == len(p) - 1 == len(q) - 1 == len(r) - 1
            assert h(start) <= c
