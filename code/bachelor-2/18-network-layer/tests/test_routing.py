"""Distance vector equals Dijkstra on random graphs, in at most n - 1 changing rounds."""
import random

import distance_vector as dv
import link_state
import town_network


def random_graph(rng, n):
    g = {}
    names = [f"R{i}" for i in range(n)]
    for i in range(1, n):                       # a random tree keeps it connected
        dv.link(g, names[i], names[rng.randrange(i)], rng.randrange(1, 10))
    for _ in range(n):
        a, b = rng.sample(names, 2)
        dv.link(g, a, b, rng.randrange(1, 10))
    return g


def test_dv_equals_dijkstra():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randrange(2, 12)
        g = random_graph(rng, n)
        tables, rounds = dv.converge(g, inf=10**6)
        assert rounds <= n - 1
        ls = link_state.tables(g)
        for u in g:
            for d in g:
                assert tables[u][d][0] == ls[u][0][d]


def test_count_to_infinity_rounds():
    g = {}
    dv.link(g, "A", "B", 1)
    dv.link(g, "B", "C", 1)
    tables, _ = dv.converge(g)
    del g["B"]["C"], g["C"]["B"]
    worst = [max(tables["A"]["C"][0], tables["B"]["C"][0])]
    for _ in range(14):
        tables = dv.dv_round(g, tables)
        worst.append(max(tables["A"]["C"][0], tables["B"]["C"][0]))
    assert worst == [2] + list(range(3, 17))   # up by the link cost each round


def test_town_loads():
    g, names = town_network.load()
    assert len(g) == len(names) == 30
