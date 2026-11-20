"""Tests for chapter 16: verifiers, search, self-reduction, Savitch, QBF, exercises."""
import itertools
import os
import random
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("listings", "exercises", "figures"):
    sys.path.insert(0, os.path.join(HERE, "..", d))

import ex5_hampath  # noqa: E402
import ex6_clique  # noqa: E402
import ex12_bipartite  # noqa: E402
import qbf  # noqa: E402
import savitch  # noqa: E402
import search_vs_verify  # noqa: E402
import self_reduce  # noqa: E402
import steps  # noqa: E402
import verifiers  # noqa: E402


def test_verifiers_accept_and_reject():
    rng = random.Random(1)
    order, edges, colour = verifiers.instance(30, rng)
    assert verifiers.hamiltonian_path(30, edges, order)[0]
    assert not verifiers.hamiltonian_path(30, edges, order[:-1] + order[:1])[0]
    assert verifiers.three_colouring(30, edges, colour)[0]
    u, v = edges[0]
    bad = list(colour)
    bad[u] = bad[v]
    assert not verifiers.three_colouring(30, edges, bad)[0]
    assert verifiers.subset_sum([3, 5, 9], 12, [0, 2])[0]
    assert not verifiers.subset_sum([3, 5, 9], 6, [0, 0])[0]  # an index twice


def test_verifier_steps_are_linear():
    rng = random.Random(2)
    for n in (10, 100, 1000):
        order, edges, colour = verifiers.instance(n, rng)
        assert verifiers.hamiltonian_path(n, edges, order)[1] == 3 * n - 1
        assert verifiers.three_colouring(n, edges, colour)[1] == 3 * n


def test_search_matches_brute_force():
    rng = random.Random(3)
    for _ in range(50):
        nums = [rng.randrange(1, 20) for _ in range(rng.randrange(1, 8))]
        t = rng.randrange(0, 60)
        brute = any(sum(c) == t for k in range(len(nums) + 1)
                    for c in itertools.combinations(nums, k))
        assert search_vs_verify.search(nums, t) == (brute, 2 ** len(nums))


def test_self_reduction_uses_n_plus_one_calls_and_exercise_4():
    rng = random.Random(4)
    for n in range(3, 10):
        clauses = [[rng.choice((1, -1)) * v for v in rng.sample(range(1, n + 1), 3)]
                   for _ in range(3 * n)]
        self_reduce.calls = 0
        a = self_reduce.find_assignment(clauses, n)
        if a is None:
            assert self_reduce.calls == 1
        else:
            assert self_reduce.calls == n + 1
            assert all(any((x > 0) == a[abs(x) - 1] for x in c) for c in clauses)


def bfs_reach(n, edges, u, v):
    return savitch.bfs(n, edges, u, v)[0]


def test_savitch_agrees_with_bfs_and_depth():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randrange(2, 9)
        edges = [(a, b) for a in range(n) for b in range(n) if a != b and rng.random() < 0.2]
        for u, v in itertools.product(range(n), repeat=2):
            s = savitch.Savitch(n, edges)
            assert s.path_exists(u, v) == bfs_reach(n, edges, u, v)
            assert s.max_depth <= max(1, (n - 1).bit_length()) + 1


def test_qbf_game():
    for m in range(1, 13):
        qs = "EA" * (m // 2) + "E" * (m % 2)
        assert qbf.value(qs, qbf.first_player_wins(m)) == (m % 3 != 0)


def test_figure_data():
    rows = steps.table(open(os.path.join(HERE, "..", "outputs",
                                         "search_vs_verify.txt")).read())
    assert rows[0] == (4, 16, 4) and all(s == 2 ** n and v == n for n, s, v in rows)


def test_exercise_5_hampath():
    edges = [(0, 1), (1, 2), (2, 3)]
    assert ex5_hampath.buggy(4, edges, [0, 1, 0, 1])
    assert not ex5_hampath.fixed(4, edges, [0, 1, 0, 1])
    assert ex5_hampath.fixed(4, edges, [3, 2, 1, 0])


def test_exercise_6_clique():
    rng = random.Random(6)
    for _ in range(200):
        n = rng.randrange(1, 7)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.6]
        for k in range(1, n + 1):
            for c in itertools.permutations(range(n), k):
                truth = all((min(a, b), max(a, b)) in edges
                            for a, b in itertools.combinations(c, 2))
                assert ex6_clique.verify_clique(n, edges, k, list(c)) == truth
    assert not ex6_clique.verify_clique(3, [(0, 1)], 2, [0, 0])


def two_colourable_bfs(n, edges):
    colour = {}
    for s in range(n):
        if s in colour:
            continue
        colour[s], queue = 0, deque([s])
        while queue:
            x = queue.popleft()
            for a, b in edges:
                for y, z in ((a, b), (b, a)):
                    if y == x:
                        if z not in colour:
                            colour[z] = 1 - colour[x]
                            queue.append(z)
                        elif colour[z] == colour[x]:
                            return False
    return True


def test_exercise_12_bipartite():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randrange(1, 7)
        edges = {(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.35}
        assert ex12_bipartite.two_colourable(n, edges) == two_colourable_bfs(n, edges)
