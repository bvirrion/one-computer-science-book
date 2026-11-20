import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def random_workload(rng):
    t, w = 0, []
    for k in range(rng.randint(1, 6)):
        t += rng.randint(0, 4)
        w.append((chr(65 + k), t, rng.randint(1, 7)))
    return w


def test_schedulers_do_all_the_work():
    sc = load("listings", "scheduler")
    rng = random.Random(1)
    for _ in range(300):
        w = random_workload(rng)
        q, s = rng.randint(1, 5), rng.randint(0, 2)
        for slices in [sc.fcfs(w, s), sc.round_robin(w, q, s)]:
            done = {}
            for name, start, end in slices:
                assert end > start
                done[name] = done.get(name, 0) + end - start
            assert done == {n: b for n, _, b in w}
            assert all(a[2] <= b[1] for a, b in zip(slices, slices[1:]))
            arrival = {n: a for n, a, _ in w}
            assert all(start >= arrival[n] for n, start, _ in slices)
            assert all(len(x) == q or x[2] - x[1] <= q
                       for x in sc.round_robin(w, q, s))


def test_listing_numbers():
    sc = load("listings", "scheduler")
    w = [("A", 0, 5), ("B", 1, 3), ("C", 2, 8), ("D", 3, 2)]
    assert sc.gantt(sc.round_robin(w, 2)) == "AABBCCAADDBCCACCCC"
    qm = load("listings", "quantum")
    best = min(range(1, 13), key=lambda q: (qm.mean_turnaround(
        sc.round_robin(qm.workload, q, 1)), q))
    assert best == 6
    assert qm.mean_turnaround(sc.fcfs(qm.workload, 1)) == 27.4


def test_interleavings_and_locks():
    il = load("listings", "interleave")
    runs = [il.run(s) for s in il.interleavings(il.steps("P"), il.steps("Q"))]
    assert len(runs) == 20 and runs.count(2) == 2
    wl = load("listings", "with_lock")
    assert set(wl.explore(wl.program("P"), wl.program("Q"))) == {2}
    dl = load("listings", "deadlock_sim")
    assert len(dl.run_pair("AB", "BA")) == 2 and dl.run_pair("AB", "AB") == []


def test_exercises():
    ex = load("exercises", "ps_ex")
    sc = load("listings", "scheduler")
    w = [("A", 0, 5), ("B", 1, 3), ("C", 2, 8), ("D", 3, 2)]
    assert ex.turnaround(w, ex.sjf(w)) == {"A": 5, "B": 9, "C": 16, "D": 4}
    slices, left = ex.round_robin_no_requeue(w, 2)
    assert left == {"A": 3, "B": 1, "C": 6, "D": 0}
    assert ex.count_interleavings(3, 3) == 20
    assert ex.has_cycle({"P": ["Q"], "Q": ["R"], "R": ["P"]})
    assert not ex.has_cycle({"P": ["Q"], "Q": ["R"], "R": []})
    assert ex.philosophers(5, False) and not ex.philosophers(5, True)
    same = [("A", 0, 6), ("B", 0, 8), ("C", 0, 3), ("D", 0, 2)]
    fcfs_wait = sum(wt for _, wt in sc.times(same, sc.fcfs(same)).values()) / 4
    sjf_wait = sum(wt for _, wt in sc.times(same, ex.sjf(same)).values()) / 4
    assert (fcfs_wait, sjf_wait) == (9.25, 4.5)
    best = min(sum(sum(b for _, _, b in order[:k]) for k in range(4)) / 4
               for order in permutations(same))
    assert best == sjf_wait


def test_problem_numbers():
    sc = load("listings", "scheduler")
    ex = load("exercises", "ps_ex")
    qm = load("listings", "quantum")
    w = qm.workload
    free = {q: qm.mean_turnaround(sc.round_robin(w, q, 0)) for q in range(1, 13)}
    assert free[1] == 17.4 and free[2] == free[3] == 17.0 == min(free.values())
    assert qm.mean_turnaround(ex.sjf(w)) == 24.0
    six = sc.round_robin(w, 6, 1)
    assert {n: e for n, _, e in six} == {"A": 40, "B": 10, "C": 17, "D": 20, "E": 25}
    for q in range(20, 30):
        assert sc.round_robin(w, q, 1) == sc.fcfs(w, 1)
    four = {n: e for n, _, e in sc.round_robin(w, 4, 1)}
    five = {n: e for n, _, e in sc.round_robin(w, 5, 1)}
    assert four == {"A": 42, "B": 8, "C": 29, "D": 16, "E": 26}
    assert five == {"A": 42, "B": 9, "C": 31, "D": 18, "E": 23}
    xyz = [("X", 0, 4), ("Y", 0, 1), ("Z", 0, 3)]
    assert sc.gantt(sc.round_robin(xyz, 1)) == "XYZXZXZX"


def test_quantum_one():
    sc = load("listings", "scheduler")
    qm = load("listings", "quantum")
    t = sc.times(qm.workload, sc.round_robin(qm.workload, 1, 1))
    assert {n: x for n, (x, _) in t.items()} == {"A": 57, "B": 20, "C": 41, "D": 16, "E": 30}
