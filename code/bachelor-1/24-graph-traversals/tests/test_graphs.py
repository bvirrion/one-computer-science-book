"""Traversals against brute force on random graphs: the parenthesis property and edge
classes, BFS distances, topological orders, strong components against the reachability
closure, bridges against removal, orientations, and the exercises."""

import itertools
import random
import sys
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from bfs import bfs  # noqa: E402
from bipartite import two_colour  # noqa: E402
from bridges import bridges, undirected_roads  # noqa: E402
from components import components  # noqa: E402
from count_paths import count_shortest  # noqa: E402
from dfs import dfs, dfs_iterative  # noqa: E402
from edge_file import read, write  # noqa: E402
from euler import euler_circuit  # noqa: E402
from find_cycle import find_cycle  # noqa: E402
from graph import Graph, friendships, roads  # noqa: E402
from kosaraju import kosaraju  # noqa: E402
from orient import orient  # noqa: E402
from topo import by_dfs, by_kahn, is_topological  # noqa: E402


def random_graph(rng, n, p, directed):
    g = Graph(directed)
    for v in range(n):
        g.add_vertex(v)
    for u, v in itertools.product(range(n), repeat=2):
        if (directed and u != v or u < v) and rng.random() < p:
            g.add_edge(u, v)
    return g


def reach(g):
    """reach[u]: the set of vertices reachable from u, by closure."""
    r = {u: {u} | set(g.adj[u]) for u in g.adj}
    changed = True
    while changed:
        changed = False
        for u in r:
            new = set().union(*(r[v] for v in r[u]))
            if not new <= r[u]:
                r[u] |= new
                changed = True
    return r


def test_dfs_parenthesis_and_classes():
    rng = random.Random(24)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 9), rng.random() * 0.5, True)
        disc, fin, parent, classes = dfs(g)
        times = sorted(list(disc.values()) + list(fin.values()))
        assert times == list(range(1, 2 * len(g.adj) + 1))

        def descendant(v, u, parent=parent):
            while v is not None:
                if v == u:
                    return True
                v = parent[v]
            return False

        for u, v in itertools.combinations(g.adj, 2):
            a, b = (disc[u], fin[u]), (disc[v], fin[v])
            disjoint = a[1] < b[0] or b[1] < a[0]
            nested_uv = a[0] < b[0] and b[1] < a[1]
            nested_vu = b[0] < a[0] and a[1] < b[1]
            assert disjoint + nested_uv + nested_vu == 1
            assert nested_uv == descendant(v, u)
        for (u, v), k in classes.items():
            if k in ("tree", "forward"):
                assert descendant(v, u) and u != v
            elif k == "back":
                assert descendant(u, v)
            else:
                assert not descendant(u, v) and not descendant(v, u)
        acyclic = all(u not in reach(g)[v] for u in g.adj for v in g.adj[u])
        assert acyclic == ("back" not in classes.values())
        assert set(dfs_iterative(g, 0)) == reach(g)[0]


def test_bfs_distances():
    rng = random.Random(7)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 9), rng.random() * 0.5, rng.random() < 0.5)
        dist, parent = bfs(g, 0)
        frontier, d, expected = {0}, 0, {}
        while frontier:  # brute force: the vertices first reached in d steps
            for v in frontier:
                expected[v] = d
            frontier = {w for v in frontier for w in g.adj[v]} - set(expected)
            d += 1
        assert dist == expected
        assert all(dist[parent[v]] == dist[v] - 1 for v in dist if v != 0)


def test_topological_orders():
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 9)
        g = Graph(directed=True)
        for v in rng.sample(range(n), n):
            g.add_vertex(v)
        for u, v in itertools.combinations(range(n), 2):  # arcs u < v: acyclic
            if rng.random() < 0.3:
                g.add_edge(u, v)
        assert is_topological(g, by_dfs(g)) and is_topological(g, by_kahn(g))
    cyclic = Graph(directed=True)
    cyclic.add_edge("a", "b"), cyclic.add_edge("b", "a")
    assert by_kahn(cyclic) is None


def test_kosaraju_against_closure():
    rng = random.Random(11)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 10), rng.random() * 0.4, True)
        r = reach(g)
        comps = kosaraju(g)
        for c in comps:
            for u, v in itertools.product(c, repeat=2):
                assert v in r[u]
        assert sum(map(len, comps)) == len(g.adj)
        index = {v: i for i, c in enumerate(comps) for v in c}
        assert all(index[u] <= index[v] for u in g.adj for v in g.adj[u])
    assert len(kosaraju(roads())) == 1


def connected_count(g, skip=None):
    h = Graph(directed=False)
    for v in g.adj:
        h.add_vertex(v)
    edges = g.edges()
    for i, (u, v) in enumerate(edges):
        if i != skip:
            h.add_edge(u, v)
    return len(components(h))


def test_bridges_against_removal_and_orientation():
    rng = random.Random(5)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 9), rng.random() * 0.6, False)
        base = connected_count(g)
        brute = {frozenset(e) for i, e in enumerate(g.edges())
                 if connected_count(g, skip=i) > base}
        assert {frozenset(e) for e in bridges(g)} == brute
        if base == 1 and not brute and len(g.adj) > 1:
            o = orient(g)
            assert len(o.edges()) == len(g.edges()) and len(kosaraju(o)) == 1
    g = undirected_roads()
    assert not bridges(g) and len(kosaraju(orient(g))) == 1
    assert len(bridges(friendships())) == 12


def test_bipartite_and_round_trip(tmp_path):
    rng = random.Random(9)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 8), rng.random() * 0.5, False)
        colour, cycle = two_colour(g)
        brute = any(all(c[u] != c[v] for u, v in g.edges())
                    for c in ({v: (m >> i) & 1 for i, v in enumerate(g.adj)}
                              for m in range(2 ** len(g.adj))))
        assert (colour is not None) == brute
        if cycle:
            assert len(cycle) % 2 == 1
            assert all(cycle[i - 1] in g.adj[cycle[i]] for i in range(len(cycle)))
        write(g, tmp_path / "g.txt")
        h = read(tmp_path / "g.txt")
        assert {v: sorted(h.adj[v]) for v in h.adj} == {v: sorted(g.adj[v]) for v in g.adj}


def test_exercises():
    rng = random.Random(13)
    for _ in range(200):
        g = random_graph(rng, rng.randint(1, 7), rng.random() * 0.6, rng.random() < 0.5)
        dist, ways = count_shortest(g.adj, 0)

        def walks(v, k, adj=g.adj):  # paths of k edges from 0 to v, enumerated
            if k == 0:
                return int(v == 0)
            return sum(walks(u, k - 1) for u in adj if v in adj[u])

        assert all(ways[v] == walks(v, dist[v]) for v in dist)
        d = random_graph(rng, rng.randint(1, 7), rng.random() * 0.5, True)
        cycle = find_cycle(d.adj)
        acyclic = all(u not in reach(d)[v] for u in d.adj for v in d.adj[u])
        assert (cycle is None) == acyclic
        if cycle:
            assert all(cycle[(i + 1) % len(cycle)] in d.adj[cycle[i]]
                       for i in range(len(cycle)))
    for _ in range(100):  # even degrees: a union of random closed walks
        n, edges = rng.randint(2, 7), []
        for _ in range(rng.randint(1, 3)):
            walk = [0] + [rng.randrange(n) for _ in range(rng.randint(1, 5))] + [0]
            edges += [(a, b) for a, b in zip(walk, walk[1:]) if a != b]
        if not edges:
            continue
        circuit = euler_circuit(edges, edges[0][0])
        assert circuit[0] == circuit[-1] and len(circuit) == len(edges) + 1
        steps = sorted(tuple(sorted(e)) for e in zip(circuit, circuit[1:]))
        assert steps == sorted(tuple(sorted(e)) for e in edges)
