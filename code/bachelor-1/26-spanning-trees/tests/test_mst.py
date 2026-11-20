"""Kruskal, Prim and Boruvka against brute force over spanning trees; union--find against a
naive oracle; bottlenecks; the exercises."""

import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from bottleneck import minimax, tree_path_max  # noqa: E402
from boruvka import boruvka  # noqa: E402
from count_trees import spanning_trees  # noqa: E402
from exo_rank_bug import Buggy, tallest  # noqa: E402
from kruskal import kruskal  # noqa: E402
from maze import maze  # noqa: E402
from prim import prim  # noqa: E402
from rank_height import pairing  # noqa: E402
from second_best import second_best  # noqa: E402
from uf_naive import Labels, Pointers  # noqa: E402
from union_find import UnionFind  # noqa: E402


def connected_graph(rng, n):
    """A random tree plus random extra edges, distinct weights."""
    weights = rng.sample(range(1, 1000), n * n)
    edges = [(weights.pop(), rng.randrange(v), v) for v in range(1, n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < 0.3:
                edges.append((weights.pop(), u, v))
    return list(range(n)), edges


def total(tree):
    return sum(w for w, _, _ in tree)


def test_mst_algorithms_against_brute_force():
    rng = random.Random(26)
    for _ in range(150):
        vertices, edges = connected_graph(rng, rng.randint(1, 7))
        trees = list(spanning_trees(vertices, edges))
        best = min(map(total, trees))
        k, _ = kruskal(vertices, edges)
        assert total(k) == best
        assert total(prim(vertices, edges, rng.choice(vertices))[0]) == best
        assert total(boruvka(vertices, edges)[0]) == best
        assert sum(total(t) == best for t in trees) == 1  # distinct weights: unique
        if len(trees) > 1:
            assert second_best(vertices, edges) == sorted(map(total, trees))[1]
        for a in vertices:  # bottleneck theorem
            direct = minimax(vertices, edges, a)
            for b in vertices:
                assert tree_path_max(k, a, b) == direct[b]
                assert direct[b] == min(max((w for w, _, _ in p), default=0)
                                        for p in paths(edges, a, b))


def paths(edges, a, b):
    """Every simple path from a to b, as lists of edges (brute force)."""
    out, stack = [], [(a, [], {a})]
    while stack:
        u, used, seen = stack.pop()
        if u == b:
            out.append(used)
            continue
        for e in edges:
            for x, y in ((e[1], e[2]), (e[2], e[1])):
                if x == u and y not in seen:
                    stack.append((y, used + [e], seen | {y}))
    return out


@settings(max_examples=200, deadline=None)
@given(st.lists(st.tuples(st.integers(0, 11), st.integers(0, 11)), max_size=30))
def test_union_find_against_naive(pairs):
    fast, labels, pointers = UnionFind(range(12)), Labels(range(12)), Pointers(range(12))
    for x, y in pairs:
        fast.union(x, y)
        labels.union(x, y)
        pointers.union(x, y)
        for a in range(12):
            for b in range(12):
                same = labels.find(a) == labels.find(b)
                assert (fast.find(a) == fast.find(b)) == same
                assert (pointers.find(a) == pointers.find(b)) == same


def test_rank_bounds():
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randint(1, 200)
        uf = UnionFind(range(n))
        for _ in range(2 * n):
            uf.union(rng.randrange(n), rng.randrange(n))
        for x in range(n):  # a root of rank r has at least 2^r elements
            if uf.parent[x] == x:
                assert sum(uf.find(y) == x for y in range(n)) >= 2 ** uf.rank[x]
    assert tallest(pairing(64)) == 6
    b = Buggy(range(50))
    for i in range(1, 50):
        b.union(i, i - 1)
    assert tallest(b) == 49


def test_maze_is_a_spanning_tree():
    for seed in range(20):
        opened = maze(6, 9, seed)
        assert len(opened) == 6 * 9 - 1
        uf = UnionFind([(r, c) for r in range(6) for c in range(9)])
        assert all(uf.union(a, b) for a, b in opened)
