import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from itertools import permutations
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def random_graph(rng, n, p, weighted=False, directed=False):
    g = {v: {} for v in range(n)}
    for a in range(n):
        for b in range(n):
            if a != b and rng.random() < p and (directed or a < b):
                w = rng.randint(1, 9) if weighted else 1
                g[a][b] = w
                if not directed:
                    g[b][a] = w
    return g


def floyd(g):
    d = {a: {b: (0 if a == b else g[a].get(b, float("inf"))) for b in g} for a in g}
    for k in g:
        for a in g:
            for b in g:
                d[a][b] = min(d[a][b], d[a][k] + d[k][b])
    return d


def test_bfs_and_dijkstra_against_floyd():
    bfs = load("listings", "bfs")
    dij = load("listings", "dijkstra")
    rng = random.Random(11)
    for _ in range(60):
        n = rng.randint(1, 12)
        unw = random_graph(rng, n, 0.25)
        d = floyd(unw)
        dist, parent = bfs.bfs({v: list(unw[v]) for v in unw}, 0)
        assert dist == {v: d[0][v] for v in unw if d[0][v] < float("inf")}
        for v in dist:
            assert len(bfs.path_to(parent, v)) == dist[v] + 1
        wg = random_graph(rng, n, 0.3, weighted=True, directed=True)
        d = floyd(wg)
        dist, _ = dij.dijkstra(wg, 0)
        assert dist == {v: d[0][v] for v in wg if d[0][v] < float("inf")}


def test_dfs_and_cycles():
    dfs = load("listings", "dfs")
    cyc = load("listings", "cycle")
    ex = load("exercises", "graphs_ex")
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 9)
        g = {v: list(ns) for v, ns in random_graph(rng, n, 0.3).items()}
        assert dfs.dfs_stack(g, 0) == dfs.dfs_rec(g, 0)
        for b in g:
            assert ex.has_path(g, 0, b) == (b in dfs.dfs_stack(g, 0))
        edges = ex.count_edges(g)
        comps = len({frozenset(dfs.dfs_stack(g, v)) for v in g})
        assert cyc.has_cycle_undirected(g) == (edges > n - comps)
        dg = {v: list(ns) for v, ns in random_graph(rng, n, 0.25, directed=True).items()}
        acyclic = any(all(order.index(a) < order.index(b) for a in dg for b in dg[a])
                      for order in permutations(dg)) if n <= 6 else None
        if acyclic is not None:
            assert cyc.has_cycle_directed(dg) == (not acyclic)
            if acyclic:
                order = ex.topological_order(dg)
                assert all(order.index(a) < order.index(b) for a in dg for b in dg[a])
            else:
                with pytest.raises(ValueError):
                    ex.topological_order(dg)


def test_listing_numbers(monkeypatch):
    monkeypatch.chdir(HERE / "listings")
    m = load("listings", "maze")
    g = m.make_maze()
    goal = (m.ROWS - 1, m.COLS - 1)
    assert load("listings", "bfs").bfs(g, (0, 0))[0][goal] == 32
    assert m.wall_follower(g, (0, 0), goal) == 58
    md = load("listings", "maze_doors")
    assert (md.cost_short, md.dist[md.goal], len(md.cheap) - 1) == (57, 54, 34)
    assert len(md.passages) == 119
    ex = load("exercises", "graphs_ex")
    d = load("listings", "bfs").bfs(g, (0, 0))[0]
    assert ex.count_shortest(g, d, (0, 0), goal) == 5
    town = load("listings", "dijkstra_town")
    assert (town.there, town.back) == (1360, 2630)
    assert load("listings", "negative_weight").brute_force(
        {"S": {"A": 1, "B": 3}, "A": {}, "B": {"A": -3}}, "S", "A") == 0


def test_exercises():
    ex = load("exercises", "graphs_ex")
    assert [ex.all_paths_calls(ex.grid(n), (0, 0)) for n in (2, 3, 4)] == [7, 79, 2111]
    W = load("listings", "dijkstra").W
    assert ex.dijkstra_last(W, "S")["T"] == 15
    G = load("listings", "representations").G
    assert ex.bfs_layers(G, "D") == [["D"], ["B", "C", "F"], ["A", "E"]]
