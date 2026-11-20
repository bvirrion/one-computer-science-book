import itertools

from hypothesis import given, settings
from hypothesis import strategies as st

from bad_example import narrowest_path
from matching import max_matching
from maxflow import Network, max_flow, min_cut, shortest_path
from town_net import town_network

networks = st.lists(st.tuples(st.integers(0, 5), st.integers(0, 5), st.integers(1, 9)),
                    max_size=14)


def build(edges):
    net = Network()
    for u, v, c in edges:
        if u != v:
            net.add_edge(u, v, c)
    return net


def brute_min_cut(net, s, t, vertices):
    best = None
    others = [v for v in vertices if v not in (s, t)]
    for k in range(len(others) + 1):
        for extra in itertools.combinations(others, k):
            side = {s, *extra}
            cap = sum(c for (u, v), c in net.cap.items() if u in side and v not in side)
            best = cap if best is None else min(best, cap)
    return best


def check_flow(net, flow, s, t, value):
    for (u, v), f in flow.items():
        assert 0 <= f <= net.cap.get((u, v), 0)
        assert isinstance(f, int)  # integrality
    for w in net.adj:
        if w not in (s, t):
            inflow = sum(f for (u, v), f in flow.items() if v == w)
            assert inflow == sum(f for (u, v), f in flow.items() if u == w)
    out = sum(f for (u, v), f in flow.items() if u == s)
    assert out - sum(f for (u, v), f in flow.items() if v == s) == value


@settings(max_examples=300, deadline=None)
@given(networks)
def test_max_flow_equals_min_cut(edges):
    net = build(edges)
    value, flow = max_flow(net, 0, 5)
    check_flow(net, flow, 0, 5, value)
    side, cut = min_cut(net, flow, 0)
    assert 5 not in side
    assert sum(net.cap[e] for e in cut) == value
    assert value == brute_min_cut(net, 0, 5, range(6))


@settings(max_examples=60, deadline=None)
@given(networks)
def test_any_path_rule_gives_the_same_value(edges):
    net = build(edges)
    assert max_flow(net, 0, 5, narrowest_path)[0] == max_flow(net, 0, 5)[0]


def test_bad_example():
    for C in [3, 10, 50]:
        net = build([("s", "a", C), ("s", "b", C), ("a", "t", C), ("b", "t", C),
                     ("a", "b", 1)])
        log1, log2 = [], []
        assert max_flow(net, "s", "t", narrowest_path, log1)[0] == 2 * C
        assert max_flow(net, "s", "t", shortest_path, log2)[0] == 2 * C
        assert (len(log1), len(log2)) == (2 * C, 2)


bipartite = st.dictionaries(st.integers(0, 6),
                            st.lists(st.sampled_from("abcdefg"), unique=True),
                            max_size=7)


def brute_matching(adj, used=frozenset()):
    """The largest matching by trying, for each left vertex, every free partner."""
    if not adj:
        return 0
    u, rest = next(iter(adj)), dict(adj)
    del rest[u]
    best = brute_matching(rest, used)  # u stays unmatched
    for v in adj[u]:
        if v not in used:
            best = max(best, 1 + brute_matching(rest, used | {v}))
    return best


@settings(max_examples=200, deadline=None)
@given(bipartite)
def test_matching_is_maximum_and_equals_flow(adj):
    match = max_matching(adj)
    assert all(u in adj and v in adj[u] for v, u in match.items())
    assert len(set(match.values())) == len(match)
    assert len(match) == brute_matching(adj)
    net = Network()
    for u, vs in adj.items():
        net.add_edge("s", ("L", u), 1)
        for v in vs:
            net.add_edge(("L", u), ("R", v), 1)
    for v in {v for vs in adj.values() for v in vs}:
        net.add_edge(("R", v), "t", 1)  # once: add_edge adds up capacities
    assert max_flow(net, "s", "t")[0] == len(match)


@settings(max_examples=200, deadline=None)
@given(bipartite)
def test_konig(adj):
    from exo_cover import vertex_cover
    match = max_matching(adj)
    cover = vertex_cover(adj, match)
    assert all(u in cover or v in cover for u in adj for v in adj[u])
    assert len(cover) == len(match)


def test_town_numbers():
    net, _ = town_network()
    value, flow = max_flow(net, 16, 15)
    assert value == 120
    assert sum(net.cap[e] for e in min_cut(net, flow, 16)[1]) == 120
