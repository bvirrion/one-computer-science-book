import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import consistency  # noqa: E402
import ex5_figure8  # noqa: E402
import ex6_compaction  # noqa: E402
import ex12_crdt  # noqa: E402
import quorum  # noqa: E402
import raft  # noqa: E402
import raft_check  # noqa: E402
import twopc  # noqa: E402


def test_consistency_table():
    models = [
        consistency.linearisable,
        consistency.sequential,
        consistency.causal,
        consistency.eventual,
    ]
    got = {n: [m(h) for m in models] for n, h in consistency.H.items()}
    assert got == {
        "H1": [True] * 4,
        "H2": [False, True, True, True],
        "H3": [False, False, True, True],
        "H4": [False, False, False, True],
    }
    # exercise 1: a stale read by the writer itself is not even sequential
    h = [("A", "w", "x", 1, 0, 1), ("A", "r", "x", 0, 2, 3)]
    assert [m(h) for m in models] == [False, False, False, True]


def test_quorums():
    for n in range(1, 7):
        for r in range(1, n + 1):
            for w in range(1, n + 1):
                assert quorum.overlap(n, r, w) == (r + w > n)
    p = 0.01
    assert round(quorum.unavailable_exact(5, 3, p), 12) == 9.8506e-6
    assert abs(quorum.unavailable_exact(5, 5, p) - (1 - 0.99**5)) < 1e-15
    # exercise 8: N = 5, R = 2, W = 4
    assert round(quorum.unavailable_exact(5, 4, p) * 1e4, 3) == 9.801
    assert round(quorum.unavailable_exact(5, 2, p), 14) == 4.96e-8


def test_raft_safety_and_bug():
    for seed in range(200):
        assert raft_check.one_run(seed)[0] == set()
    broken, committed, _ = ex5_figure8.scenario(True)
    assert broken == {"state machine safety"} and len(committed[2]) == 2
    broken, committed, _ = ex5_figure8.scenario(False)
    assert broken == set() and committed[2] == [(2, "c")]


def test_raft_transcripts():
    net, servers = raft.cluster(seed=26)
    net.run(until=120)
    assert net.leaders == [(1, "S5")]


@settings(max_examples=200, deadline=None)
@given(st.lists(st.tuples(st.integers(0, 3), st.integers(0, 50)), max_size=40))
def test_compaction_matches_full_log(ops):
    full, log, term = [], ex6_compaction.CompactLog(), 1
    for kind, x in ops:
        if kind == 0:
            full.append((term, (f"k{x % 3}", x)))
            log.append(term, (f"k{x % 3}", x))
        elif kind == 1:
            term += 1
        elif kind == 2 and full:
            log.compact(x % (len(full) + 1))
        n = len(full)
        assert log.last() == (n, full[-1][0] if full else 0)
        for i in range(log.base, n + 1):
            assert log.term_at(i) == (full[i - 1][0] if i else 0)
            for t in range(term + 1):
                assert log.matches(i, t) == (log.term_at(i) == t)
        state = {}
        for _, (k, v) in full[: log.base]:
            state[k] = v
        assert log.state == state
    # a follower far behind installs the leader's snapshot
    f = ex6_compaction.CompactLog()
    f.append(1, ("k0", 1))
    f.install(log.base, log.base_term, log.state)
    assert (f.base, f.state) == (log.base, log.state) or log.base == 0


def test_crdt():
    rng = random.Random(1)
    for seed in range(50):
        made, seen = ex12_crdt.simulate(ex12_crdt.GCounter, seed)
        assert seen == [made] * 3
    made, seen = ex12_crdt.simulate(ex12_crdt.LWWRegister, 12)
    assert (made, seen) == (207, [85, 85, 85])
    a, b, c = (ex12_crdt.GCounter() for _ in range(3))
    for x, r in ((a, "R1"), (b, "R2"), (c, "R3"), (a, "R1")):
        x.increment(0, r)
    for _ in range(20):  # merge is commutative, associative and idempotent
        x, y = rng.sample([a, b, c], 2)
        x.merge(y)
    for x in (a, b, c):
        for y in (a, b, c):
            x.merge(y)
    assert a.counts == b.counts == c.counts and a.value == 4


def test_twopc():
    notes = twopc.run((1, 1, 1), crash=True).notes
    assert sum("commit, locks held" in n for n in notes) == 3
    assert any("asked 14 times" in n for n in notes)
    assert sum("abort" in n for n in twopc.run((1, 0, 1)).notes) == 4


def test_exercises_2_3_and_problem():
    def both_work(n, r, w):
        return min(n - r, n - w)

    got = [
        (quorum.overlap(n, r, w), both_work(n, r, w))
        for n, r, w in [(3, 1, 3), (4, 2, 2), (4, 2, 3), (7, 4, 4), (6, 3, 3)]
    ]
    assert got == [(True, 0), (False, 2), (True, 1), (True, 3), (False, 3)]
    logs = {
        "S1": [1, 1, 2],
        "S2": [1, 1, 2, 3],
        "S3": [1, 1],
        "S4": [1, 1, 2, 2],
        "S5": [1, 1, 3],
    }

    def key(log):
        return (log[-1], len(log))

    winners = {c for c in logs if sum(key(logs[v]) <= key(logs[c]) for v in logs) >= 3}
    assert winners == {"S2", "S4", "S5"}
    out = (HERE / "outputs" / "raft_partition.txt").read_text()
    assert (
        "S5 leader    term=1 commit=1" in out and "S1 follower  term=1 commit=1" in out
    )
    assert out.count("term=2 commit=2") == 8  # three at t=199, all five at t=260


def test_solution_8_and_problem_numbers():
    p = 0.01
    r2, w4 = quorum.unavailable_exact(5, 2, p), quorum.unavailable_exact(5, 4, p)
    assert round((1000 * r2 + w4) / 1001 * 1e6, 1) == 1.0
    w3, w5 = quorum.unavailable_exact(5, 3, p), quorum.unavailable_exact(5, 5, p)
    assert round(w5 / w3, -2) == 5000 and round(w5, 3) == 0.049
    assert 207 - 85 == 122
