"""Dijkstra, Bellman--Ford and Floyd--Warshall against one another and against brute
force on random graphs; DAG paths; the exercises."""

import itertools
import random
import sys
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from at_most_k import at_most_k  # noqa: E402
from bellman_ford import bellman_ford  # noqa: E402
from centre import eccentricities  # noqa: E402
from dag_count import count_paths  # noqa: E402
from dag_paths import TASKS, critical_path  # noqa: E402
from dijkstra import dijkstra, path  # noqa: E402
from exo_floyd_inner import floyd_k_inner  # noqa: E402
from exo_settle_push import dijkstra_push  # noqa: E402
from floyd import floyd_warshall, route  # noqa: E402
from negative_cycle import negative_cycle  # noqa: E402
from wgraph import roads  # noqa: E402
from widest import widest  # noqa: E402

INF = float("inf")


def random_graph(rng, n, p, low, high):
    return {u: [(v, rng.randint(low, high)) for v in range(n)
                if v != u and rng.random() < p] for u in range(n)}


def simple_paths(adj, s, t):
    """Every simple path from s to t, as a list of vertices (brute force)."""
    out, stack = [], [[s]]
    while stack:
        p = stack.pop()
        if p[-1] == t:
            out.append(p)
            continue
        stack += [p + [v] for v, _ in adj[p[-1]] if v not in p]
    return out


def weight(adj, p):
    w = {(u, v): c for u in adj for v, c in adj[u]}
    return sum(w[a] for a in zip(p, p[1:]))


def test_dijkstra_against_brute_force_and_the_others():
    rng = random.Random(25)
    for _ in range(150):
        adj = random_graph(rng, rng.randint(1, 7), rng.random() * 0.6, 0, 9)
        dist, parent, _ = dijkstra(adj, 0)
        order, d, nxt = floyd_warshall(adj)
        bf = bellman_ford(adj, 0)[0]
        for t in adj:
            paths = simple_paths(adj, 0, t)
            best = min((weight(adj, p) for p in paths), default=INF)
            assert dist[t] == best == bf[t] == d[0][order.index(t)]
            if best < INF:
                assert weight(adj, path(parent, t)) == best
                assert weight(adj, route(order, nxt, 0, t)) == best
        assert floyd_k_inner(adj) is not None


def test_negative_weights():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 6)
        adj = random_graph(rng, n, rng.random() * 0.6, -4, 9)
        cyc = negative_cycle(adj)
        brute = None
        for k in range(2, n + 1):  # every cycle, by its vertices in order
            for vs in itertools.permutations(range(n), k):
                arcs = list(zip(vs, vs[1:] + vs[:1]))
                w = {(u, v): c for u in adj for v, c in adj[u]}
                if all(a in w for a in arcs) and sum(w[a] for a in arcs) < 0:
                    brute = vs
        assert (cyc is None) == (brute is None)
        w = {(u, v): c for u in adj for v, c in adj[u]}
        if cyc:
            arcs = list(zip(cyc, cyc[1:] + cyc[:1]))
            assert all(a in w for a in arcs) and sum(w[a] for a in arcs) < 0
        result = bellman_ford(adj, 0)
        reach_neg = cyc is not None and any(
            simple_paths(adj, 0, v) for v in cyc)
        if result is None:
            assert cyc is not None
        elif not reach_neg:
            for t in adj:
                best = min((weight(adj, p) for p in simple_paths(adj, 0, t)), default=INF)
                assert result[0][t] == best


def test_at_most_k_and_widest():
    rng = random.Random(8)
    for _ in range(150):
        adj = random_graph(rng, rng.randint(1, 6), rng.random() * 0.6, -3, 9)
        k = rng.randint(0, 5)
        walks = {0: 0}
        frontier = {0: 0}
        for _ in range(k):  # brute force over walks of at most k arcs
            new = {}
            for u, d in frontier.items():
                for v, w in adj[u]:
                    new[v] = min(new.get(v, INF), d + w)
            frontier = new
            for v, d in new.items():
                walks[v] = min(walks.get(v, INF), d)
        got = at_most_k(adj, 0, k)
        assert all(got[v] == walks.get(v, INF) for v in adj)
        cap = random_graph(rng, rng.randint(1, 6), rng.random() * 0.6, 1, 9)
        width = widest(cap, 0)
        for t in cap:
            if t == 0:
                continue
            best = 0
            for p in simple_paths(cap, 0, t):
                c = {(u, v): x for u in cap for v, x in cap[u]}
                best = max(best, min(c[a] for a in zip(p, p[1:])))
            assert width[t] == best


def test_dag_paths_and_counts():
    start, length, crit = critical_path(TASKS)
    assert length == 13 and crit[0] == "design" and crit[-1] == "launch"
    for t, (_, before) in TASKS.items():
        assert all(start[b] + TASKS[b][0] <= start[t] for b in before)
    rng = random.Random(6)
    for _ in range(150):
        n = rng.randint(1, 7)
        adj = {u: [(v, rng.randint(0, 4)) for v in range(u + 1, n) if rng.random() < 0.5]
               for u in range(n)}
        dist, ways = count_paths(adj, list(range(n)), 0)
        for t in adj:
            paths = simple_paths(adj, 0, t)
            best = min((weight(adj, p) for p in paths), default=INF)
            assert dist[t] == best
            assert ways[t] == sum(weight(adj, p) == best for p in paths)


def test_town():
    adj = roads()
    order, d, _ = floyd_warshall(adj)
    ecc = eccentricities(order, d)
    assert min(ecc.values()) == 349 and max(ecc.values()) == 675
    assert dijkstra_push({"s": [("a", 5), ("b", 1)], "b": [("a", 1)], "a": []}, "s")["a"] == 5
