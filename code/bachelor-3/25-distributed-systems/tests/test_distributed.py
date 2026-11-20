import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import ex5_vclock_bug  # noqa: E402
import ex6_causal  # noqa: E402
import ex10_nonfifo  # noqa: E402
import ex12_exactly_once  # noqa: E402
import generals  # noqa: E402
import lamport  # noqa: E402
import rpc_demo  # noqa: E402
import snapshot  # noqa: E402
import vclock  # noqa: E402
from netsim import Net, Process  # noqa: E402


def random_run(choices):
    """A run of three processes built from a list of integers."""
    run, pending, n = [], {p: [] for p in vclock.PROCS}, 0
    for c in choices:
        p = vclock.PROCS[c % 3]
        kind = ("local", "send", "recv")[(c // 3) % 3]
        if kind == "recv" and not pending[p]:
            kind = "local"
        if kind == "send":
            n += 1
            pending[vclock.PROCS[(c // 9) % 3]].append(f"m{n}")
            run.append((f"e{len(run)}", p, "send", f"m{n}"))
        elif kind == "recv":
            m = pending[p].pop((c // 9) % len(pending[p]))
            run.append((f"e{len(run)}", p, "recv", m))
        else:
            run.append((f"e{len(run)}", p, "local", None))
    return run


@settings(max_examples=200, deadline=None)
@given(st.lists(st.integers(0, 10**6), max_size=30))
def test_clock_condition_and_vector_clocks_characterise(choices):
    run = random_run(choices)
    L, V = lamport.lamport(run), vclock.vector_clocks(run)
    hb = lamport.happened_before(run)
    events = [e for e, *_ in run]
    assert all(L[e] < L[f] for e, f in hb)
    for e in events:
        for f in events:
            assert vclock.before(V[e], V[f]) == ((e, f) in hb)
    # exercise 8: the test needs only the sender's own entry
    proc = {e: vclock.PROCS.index(p) for e, p, *_ in run}
    for e in events:
        for f in events:
            if e != f:
                assert ((e, f) in hb) == (V[e][proc[e]] <= V[f][proc[e]])
    # exercise 7: Lamport time, ties broken by process, totally orders the events
    key = {e: (L[e], p) for e, p, *_ in run}
    assert len(set(key.values())) == len(events)


def test_recorded_run_numbers():
    L, V = lamport.lamport(lamport.RUN), vclock.vector_clocks(lamport.RUN)
    assert [L[e] for e in ("a1", "a2", "a3", "a4")] == [1, 2, 7, 8]
    assert [L[e] for e in ("c1", "c2", "c3")] == [1, 5, 9]
    assert len(lamport.happened_before(lamport.RUN)) == 43
    assert V["c3"] == [4, 4, 3] and V["a3"] == [3, 4, 0]


def test_buggy_vector_clock():
    run = lamport.RUN
    hb = lamport.happened_before(run)
    for fn, ok in (
        (ex5_vclock_bug.vector_clocks_buggy, False),
        (ex5_vclock_bug.vector_clocks_fixed, True),
    ):
        V = fn(run)
        wrong = [
            (e, f)
            for e, *_ in run
            for f, *_ in run
            if vclock.before(V[e], V[f]) != ((e, f) in hb)
        ]
        assert (not wrong) == ok
    V = ex5_vclock_bug.vector_clocks_buggy(run)
    assert V["a2"] == V["b1"] == [2, 0, 0]  # a send and its receive get one stamp


def test_netsim_is_deterministic():
    class Ping(Process):
        def on_start(self):
            self.send("b" if self.name == "a" else "a", "x")

        def on_message(self, src, msg):
            if self.net.now < 50:
                self.send(src, msg)

    logs = []
    for _ in range(2):
        net = Net(seed=7, loss=0.1)
        net.add(Ping("a"), Ping("b"))
        logs.append(net.run().log)
    assert logs[0] == logs[1] and len(logs[0]) > 10


def test_generals():
    for k in range(1, 9):
        assert generals.check(k) == (1, 0)


def test_rpc_duplicates():
    assert rpc_demo.demo(False, (2,), port=45111) == (4, 40)
    assert rpc_demo.demo(True, (2,), port=45113) == (3, 30)
    assert rpc_demo.demo(False, (2, 3), port=45115) == (5, 50)  # exercise 4
    assert rpc_demo.demo(True, (2, 3), port=45117) == (3, 30)


def test_snapshots():
    bank = snapshot.Bank(seed=25)
    cl, naive = bank.run()
    assert cl == [5000] * 100 and all(t < 5000 for t in naive)
    markers = sum(
        1 for _, k, _, _, m in bank.net.log if k == "send" and m[0] == "marker"
    )
    assert markers == 100 * 5 * 4  # exercise 9: n(n - 1) per snapshot
    assert ex10_nonfifo.run(25, False) == (98, 0)
    assert ex10_nonfifo.run(25, True) == (0, 0)
    for seed in range(5):
        assert snapshot.Bank(seed).run()[0] == [5000] * 100
        assert ex10_nonfifo.run(seed, True) == (0, 0)


def test_causal_broadcast():
    bad = {
        c: sum(ex6_causal.violates(ex6_causal.run(s, c)["P3"]) for s in range(200))
        for c in (False, True)
    }
    assert bad == {False: 20, True: 0}
    for s in range(50):  # everything is delivered everywhere
        out = ex6_causal.run(s, True)
        assert all(sorted(v) == ["P1#1", "P1#2", "P1#3", "P2#1"] for v in out.values())


def test_exactly_once():
    with tempfile.TemporaryDirectory() as d:
        got = {
            (a, p): ex12_exactly_once.trial(f"{d}/{a}{i}.db", a, p)
            for a in (False, True)
            for i, p in enumerate(ex12_exactly_once.POINTS)
        }
    assert got[(False, "after executing")] == 2
    assert sum(got.values()) == 7


EX1 = [
    ("x1", "P1", "send", "n1"),
    ("y1", "P2", "local", None),
    ("z1", "P3", "send", "n3"),
    ("y2", "P2", "recv", "n1"),
    ("y3", "P2", "send", "n2"),
    ("x2", "P1", "recv", "n3"),
    ("z2", "P3", "recv", "n2"),
]


def consistent(run, counts):
    inside = set()
    for p, c in zip(vclock.PROCS, counts):
        inside |= set([e for e, q, *_ in run if q == p][:c])
    sent = {m: e for e, _, k, m in run if k == "send"}
    recv = {m: e for e, _, k, m in run if k == "recv"}
    ok = all(sent[m] in inside for m, e in recv.items() if e in inside)
    transit = sorted(
        m for m, e in sent.items() if e in inside and recv[m] not in inside
    )
    return ok, transit


def test_exercises_1_to_3_and_problem():
    L, V = lamport.lamport(EX1), vclock.vector_clocks(EX1)
    assert L == {"x1": 1, "y1": 1, "z1": 1, "y2": 2, "y3": 3, "x2": 2, "z2": 4}
    assert V["x2"] == [2, 0, 1] and V["z2"] == [1, 3, 2] and V["y3"] == [1, 3, 0]
    hb = lamport.happened_before(EX1)
    assert ("x1", "z2") in hb and ("z1", "x2") in hb
    assert not {("x2", "z2"), ("z2", "x2"), ("y1", "x2"), ("x2", "y1")} & hb
    run = lamport.RUN
    assert consistent(run, (2, 2, 1)) == (True, ["m2"])
    assert consistent(run, (4, 4, 2)) == (True, ["m4"])
    assert not consistent(run, (1, 1, 1))[0] and not consistent(run, (3, 3, 2))[0]
    V = vclock.vector_clocks(run)
    assert vclock.before(V["b3"], V["a4"])
    events = [e for e, *_ in run]
    conc = [
        (e, f)
        for i, e in enumerate(events)
        for f in events[i + 1 :]
        if not vclock.before(V[e], V[f]) and not vclock.before(V[f], V[e])
    ]
    assert len(conc) == 12 and len(lamport.happened_before(run)) == 43 == 55 - 12
    bank = snapshot.Bank(seed=25)
    cl, naive = bank.run()
    assert (5000 - max(naive), 5000 - min(naive)) == (145, 680)
    s50 = sum(b.snaps[50]["channels"] for b in bank.branches)
    assert s50 == 245 and bank.branches[1].snaps[99]["balance"] == 1529


def test_transfer_rate():
    bank = snapshot.Bank(seed=25)
    bank.run()
    t = [t for t, k, _, _, m in bank.net.log if k == "send" and m[0] == "money"]
    assert len(t) == 1000 and max(t) == 511
    assert sum(b.snaps[0]["balance"] for b in bank.branches) == 4775
