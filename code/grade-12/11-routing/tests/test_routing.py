import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def random_graph(rng, n):
    names = [chr(65 + k) for k in range(n)]
    g = {v: {} for v in names}
    for k in range(1, n):                        # a random tree keeps it connected
        u, v = names[k], names[rng.randrange(k)]
        g[u][v] = g[v][u] = rng.randint(1, 20)
    for _ in range(n):
        u, v = rng.sample(names, 2)
        g[u][v] = g[v][u] = rng.randint(1, 20)
    return g


def test_distance_vector_matches_dijkstra():
    dv = load("listings", "dv_rounds")
    ls = load("listings", "link_state")
    rng = random.Random(2)
    for _ in range(100):
        g = random_graph(rng, rng.randint(2, 8))
        tables, _ = dv.converge(g, {r: {r: (0, r)} for r in g})
        for r in g:
            assert {d: c for d, (c, _) in tables[r].items()} == \
                   {d: c for d, (c, _) in ls.table(g, r).items()}


def test_after_k_rounds_shortest_with_k_links():
    dv = load("listings", "dv_rounds")
    rng = random.Random(3)
    for _ in range(50):
        g = random_graph(rng, rng.randint(2, 7))
        tables = {r: {r: (0, r)} for r in g}
        best = {r: {r: 0} for r in g}            # shortest with at most k links
        for _ in range(len(g)):
            tables = dv.dv_round(g, tables)
            best = {r: {d: min([best[r].get(d, 10**9)] + [c + best[n][d] for n, c in
                                g[r].items() if d in best[n]])
                        for d in g if d in best[r] or any(d in best[n] for n in g[r])}
                    for r in g}
            for r in g:
                assert {d: c for d, (c, _) in tables[r].items()} == best[r]


def test_listing_numbers():
    ci = load("listings", "count_to_infinity")
    with redirect_stdout(io.StringIO()):
        assert ci.after_failure(False) == 15
        assert ci.after_failure(True) == 2
    ls = load("listings", "link_state")
    net = load("listings", "network")
    g = net.graph(net.by_rate)
    known, messages = ls.flood(g)
    edges = sum(len(v) for v in g.values()) // 2
    assert messages == len(g) * (2 * edges - (len(g) - 1)) == 84


def test_exercises():
    ex = load("exercises", "rt_ex")
    r = ex.routes()
    assert r["hops"] == (["A", "C", "E", "G"], 3)
    assert r["cost"] == (["A", "B", "D", "F", "G"], 130)
    assert r["cut B-D"] == (["A", "B", "C", "E", "D", "F", "G"], 1050)
    assert [ex.rounds_from_scratch(ex.line(n)) for n in range(2, 9)] == list(range(1, 8))
    assert all(ex.flood_messages(ex.ring(n)) == n * (n + 1) for n in range(3, 12))
    assert ex.cost_from_rate(100_000, 10_000) == 1 and ex.cost_from_rate(100, 10_000) == 100
    cut4 = ex.line(4)
    del cut4["R3"]["R4"], cut4["R4"]["R3"]
    assert ex.count_rounds(ex.line(4), cut4, "R4")[0] == 15
    assert ex.count_rounds(ex.line(4), cut4, "R4", poison=True)[0] == 3
    cut3 = ex.line(3)
    del cut3["R2"]["R3"], cut3["R3"]["R2"]
    assert ex.count_rounds(ex.line(3), cut3, "R3", poison=True)[0] == 2
    g = ex.graph(ex.by_rate)
    t = {v: {v: (0, v)} for v in g}
    seen = []
    for _ in range(8):
        t = ex.dv_round_larger(g, t)
        seen.append(t["A"].get("E", (0,))[0])
    assert seen[-1] > seen[-3] > seen[-5]          # never settles
    a = {"A": (0, "A")}
    assert ex.dv_update(a, "B", {"B": (0, "B"), "C": (5, "C")}, 2) == \
        {"A": (0, "A"), "B": (2, "B"), "C": (7, "B")}


def test_triangle_still_counts_with_split_horizon():
    ci = load("listings", "count_to_infinity")
    g = {"A": {"B": 1, "D": 1}, "B": {"A": 1, "D": 1, "C": 1}, "C": {"B": 1},
         "D": {"A": 1, "B": 1}}
    t = {r: {r: (0, r)} for r in g}
    for _ in range(4):
        t = ci.dv_round(g, t, True)
    cut = {"A": {"B": 1, "D": 1}, "B": {"A": 1, "D": 1}, "C": {}, "D": {"A": 1, "B": 1}}
    seen = []
    for _ in range(16):
        t = ci.dv_round(cut, t, True)
        seen.append(min(t[r].get("C", (16,))[0] for r in "ABD"))
    assert seen[0] == 2 and seen[13] == 15 and seen[14] == seen[15] == 16
    assert seen == sorted(seen)
