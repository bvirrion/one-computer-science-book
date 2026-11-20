import random
import subprocess
import sys
from itertools import permutations
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import crash_all  # noqa: E402
import doctors  # noqa: E402
import ex5_redo  # noqa: E402
import ex6_waitdie  # noqa: E402
import ex8_count  # noqa: E402
import mvcc  # noqa: E402
import schedules  # noqa: E402
import twopl  # noqa: E402
from minidb import recover  # noqa: E402


def conflict_pairs(s):
    """The ordered pairs of transactions given by the conflicts of s."""
    return {
        (s[i][0], s[j][0])
        for i in range(len(s))
        for j in range(i + 1, len(s))
        if schedules.conflict(s[i], s[j])
    }


def serial(s, order):
    return [op for t in order for op in s if op[0] == t]


def view_serialisable(s):
    def view(x):
        reads, last = [], {}
        for t, a, item in x:
            if a == "R":
                reads.append((t, item, last.get(item)))
            else:
                last[item] = t
        return sorted(reads), last

    return any(view(serial(s, o)) == view(s) for o in permutations({op[0] for op in s}))


ops = st.lists(
    st.tuples(st.integers(1, 3), st.sampled_from("RW"), st.sampled_from("AB")),
    max_size=9,
)


@settings(max_examples=300, deadline=None)
@given(ops)
def test_precedence_theorem(s):
    order = schedules.serial_order(s)
    eq = [
        o
        for o in permutations({op[0] for op in s})
        if conflict_pairs(serial(s, o)) >= conflict_pairs(s)
    ]
    assert (order is not None) == bool(eq)
    if order is not None:
        assert conflict_pairs(serial(s, order)) >= conflict_pairs(s)


def test_listing_verdicts():
    got = {
        n: schedules.serial_order(schedules.parse(t))
        for n, t in schedules.SCHEDULES.items()
    }
    assert got["serial"] == got["interleaved"] == [1, 2]
    assert all(
        got[n] is None for n in ("lost update", "crossed", "three", "blind writes")
    )
    assert view_serialisable(schedules.parse(schedules.SCHEDULES["blind writes"]))


def test_exercise_1():
    verdicts = [
        schedules.serial_order(schedules.parse(t))
        for t in (
            "R1(A) R2(B) W1(B) W2(A)",
            "R1(A) W1(A) R2(A) R1(B) W1(B) W2(B)",
            "R2(A) R1(B) W2(A) R3(A) W1(B) W3(B) R2(B)",
        )
    ]
    assert verdicts == [None, [1, 2], None]


def run_exact(text):
    """Can strict 2PL run this schedule (with Cn for commits) exactly as written?"""
    steps = text.split()
    progs = {}
    for op in steps:
        t = int(op[1 : op.index("(")] if "(" in op else op[1:])
        progs.setdefault(t, []).append((op[0], op[3:-1] if "(" in op else None))
    s = twopl.Scheduler(progs, verbose=False)
    for op in steps:
        t = int(op[1 : op.index("(")] if "(" in op else op[1:])
        if not s.step(t):
            return False
    return True


def test_exercise_2():
    assert [
        run_exact(x)
        for x in (
            "R1(A) R2(A) W1(B) W2(C) C1 C2",
            "R1(A) W2(A) C1 C2",
            "W1(A) C1 R2(A) W2(A) C2",
            "R1(A) W1(A) R2(A) W2(A) R1(B) W1(B) R2(B) W2(B) C1 C2",
        )
    ] == [True, False, True, False]


@settings(max_examples=150, deadline=None)
@given(
    st.lists(
        st.lists(
            st.tuples(st.sampled_from("RW"), st.sampled_from("ABC")),
            min_size=1,
            max_size=4,
        ),
        min_size=2,
        max_size=3,
    ),
    st.lists(st.integers(1, 3), max_size=12),
)
def test_2pl_histories_serialisable(progs, order):
    p = {t + 1: ops + [("C", None)] for t, ops in enumerate(progs)}
    s = twopl.Scheduler(p, verbose=False).run([t for t in order if t in p])
    h = [op for op in s.history if op[0] not in s.aborted]
    assert schedules.serial_order(h) is not None
    assert set(s.done) | set(s.aborted) == set(p)


@settings(max_examples=150, deadline=None)
@given(
    st.lists(
        st.lists(
            st.tuples(st.sampled_from("RW"), st.sampled_from("ABC")),
            min_size=1,
            max_size=4,
        ),
        min_size=2,
        max_size=3,
    ),
    st.lists(st.integers(1, 3), max_size=12),
)
def test_wait_die_never_deadlocks(progs, order):
    p = {t + 1: ops + [("C", None)] for t, ops in enumerate(progs)}
    s = ex6_waitdie.WaitDie(p, verbose=False)
    edges = []
    s.on_wait = lambda t, f=s.on_wait: (
        f(t),
        edges.extend((t, u) for u in s.waits.get(t, ())),
    )
    s.run([t for t in order if t in p])
    assert all(t < u for t, u in edges)  # only older waits for younger
    assert "deadlock" not in " ".join(s.log)


def test_mvcc_and_doctors(capsys):
    s = mvcc.Store({"x": 1})
    a, b = s.begin("a"), s.begin("b")
    a.write("x", 2)
    b.write("x", 3)
    a.commit()
    assert "aborts" in b.commit()
    table = {}
    for name, run in (
        ("si", doctors.run_mvcc),
        ("mat", lambda o: doctors.run_mvcc(o, materialise=True)),
        ("ssi", lambda o: doctors.run_mvcc(o, ssi=True)),
        ("2pl", doctors.run_2pl),
    ):
        r = [run(o) for o in doctors.orders()]
        table[name] = (sum(x for x, _ in r), sum(y > 0 for _, y in r))
    assert table == {"si": (68, 0), "mat": (0, 68), "ssi": (0, 68), "2pl": (0, 48)}
    died = sum(
        bool(
            ex6_waitdie.WaitDie(
                {
                    1: twopl.program("R(A) R(B) W(A) C"),
                    2: twopl.program("R(A) R(B) W(B) C"),
                },
                verbose=False,
            )
            .run(o)
            .aborted
        )
        for o in doctors.orders()
    )
    assert died == 52


def test_recovery_everywhere():
    db = crash_all.workload()
    assert len(db.events) == 23
    for _, _, (log, pages) in db.events:
        values, full = recover(log, pages)
        assert values == crash_all.expected(log)
        clrs = sum(r["kind"] == "clr" for r in full) - sum(
            r["kind"] == "clr" for r in log
        )
        for k in range(clrs):
            _, partial = recover(log, pages, crash_after=k)
            again, twice = recover(partial, pages)
            assert again == crash_all.expected(log)
            assert recover(twice, pages)[0] == again  # and once more


def test_random_workloads():
    rng = random.Random(23)
    for _ in range(300):
        db = crash_all.MiniDB(crash_all.INITIAL)
        live, owner = set(), {}  # owner: the exclusive locks of strict 2PL
        for _ in range(25):
            t = rng.randint(1, 5)
            act = rng.random()
            if t in db.last and act < 0.22:
                db.commit(t) if act < 0.15 else db.rollback(t)
                owner = {k: u for k, u in owner.items() if u != t}
            elif act < 0.35:
                db.write_page(rng.randrange(4))
            elif act < 0.4:
                db.checkpoint()
            elif t not in live or t in db.last:
                item = rng.choice("abcdefgh")
                if owner.setdefault(item, t) == t:
                    live.add(t)
                    db.update(t, item, rng.randint(1, 99))
        for _, _, (log, pages) in db.events:
            assert recover(log, pages)[0] == crash_all.expected(log)


def test_exercise_5():
    assert ex5_redo.failures(ex5_redo.redo_committed) == [(14, "log", 12, {"e": 30})]
    assert ex5_redo.failures(ex5_redo.redo) == []


def test_exercise_8():
    assert [ex8_count.brute(k) for k in (1, 2, 3)] == [2, 12, 106]
    assert [ex8_count.by_rule(k) for k in (1, 2, 3)] == [2, 12, 106]


def test_sqlite_steps():
    out = subprocess.run(
        [sys.executable, str(HERE / "listings" / "sqlite_isolation.py")],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert out.count("B: BEGIN IMMEDIATE -> error: database is locked") == 2
    assert "A: COMMIT -> error: database is locked" in out
    assert out[-1].endswith("-> 2")


def test_solution_numbers():
    def holds(o):
        a = [i for i, t in enumerate(o) if t == 1]
        b = [i for i, t in enumerate(o) if t == 2]
        return b[0] < a[2] and a[1] < b[2]  # each reads what the other then writes

    progs = {1: "R(A) R(B) W(A) C", 2: "R(A) R(B) W(B) C"}
    deadlocked, died = set(), set()
    for o in doctors.orders():
        if doctors.run_2pl(o)[1]:
            deadlocked.add(tuple(o))
        p = {t: twopl.program(x) for t, x in progs.items()}
        if ex6_waitdie.WaitDie(p, verbose=False).run(o).aborted:
            died.add(tuple(o))
        assert (tuple(o) in deadlocked) == holds(o)
    assert len(deadlocked) == 48 and deadlocked < died and len(died - deadlocked) == 4
    assert all(o[:3] == (1, 1, 1) for o in died - deadlocked)
    assert [ex8_count.brute(4)] == [1108]


def test_one_abort_each():
    for o in doctors.orders():
        serial = o in ([1] * 4 + [2] * 4, [2] * 4 + [1] * 4)
        for kw in ({"ssi": True}, {"materialise": True}):
            assert doctors.run_mvcc(o, **kw)[1] == (0 if serial else 1)
