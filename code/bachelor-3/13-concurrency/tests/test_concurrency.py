import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "listings"), str(HERE.parent / "exercises")]

import aba_replay  # noqa: E402
import banker  # noqa: E402
import ex6_detect  # noqa: E402
import linearizable  # noqa: E402
import monitor_sim  # noqa: E402
import philosophers  # noqa: E402
import rag_cycle  # noqa: E402
import waiter  # noqa: E402


def pell_lucas(n):
    a, b = 2, 2  # Q(0), Q(1)
    for _ in range(n):
        a, b = b, 2 * b + a
    return a


def test_naive_states_are_pell_lucas_with_one_deadlock():
    for n in range(2, 10):
        seen, dead = philosophers.explore(n)
        assert len(seen) == pell_lucas(n)
        assert dead == [((philosophers.HOLD1,) * n, tuple(range(n)))]


def test_ordered_never_deadlocks():
    for n in range(2, 10):
        assert philosophers.explore(n, ordered=True)[1] == []


def test_exercise_4_three_philosophers():
    seen, dead = philosophers.explore(3)
    assert len(seen) == 14 and dead == [((1, 1, 1), (0, 1, 2))]


def test_waiter_no_deadlock_and_a_valid_starving_walk():
    for n in range(3, 8):
        assert waiter.explore(n)[1] == 0
    n, walk = 5, waiter.starving_cycle(5)
    here = walk[-1][1]
    reachable = waiter.explore(n)[0]
    assert here in reachable
    for i, nxt in walk:
        assert (i, nxt) in list(waiter.moves(here, n)) and i != 0
        assert nxt[0] == waiter.HUNGRY and not waiter.can_eat(nxt, 0, n)
        here = nxt
    assert {i for i, _ in walk} == {1, 2, 3, 4}


def test_banker_example_and_exercise_1():
    alloc = [[1, 1, 0], [2, 0, 1], [0, 1, 1], [1, 0, 2], [0, 2, 0]]
    need = [[3, 1, 2], [1, 2, 1], [2, 2, 2], [1, 1, 1], [3, 1, 1]]
    assert banker.safe_order([2, 1, 2], alloc, need) == [3, 0, 1, 2, 4]
    assert banker.request(1, [1, 0, 0], [2, 1, 2], alloc, need) is None
    # exercise 1: one kind of resource, 12 units
    assert banker.safe_order([3], [[5], [2], [2]], [[5], [2], [7]]) == [1, 0, 2]
    assert banker.safe_order([2], [[5], [2], [3]], [[5], [2], [6]]) is None
    assert banker.safe_order([2], [[5], [3], [2]], [[5], [1], [7]]) == [1, 0, 2]


def test_rag_cycle_and_exercise_2():
    g = {"P1": ["R1"], "R1": ["P2"], "P2": ["R2"], "R2": ["P3"], "P3": ["R3"],
         "R3": ["P1"], "P4": ["R1"]}
    assert rag_cycle.find_cycle(g) == ["P1", "R1", "P2", "R2", "P3", "R3", "P1"]
    g["R3"] = []
    assert rag_cycle.find_cycle(g) is None


def test_exercise_6_detection():
    d = ex6_detect.deadlocked
    # P2 finishes and frees a unit of kind 0, which lets P1 and then P0 finish
    assert d([0, 0], [[1, 0], [0, 1], [1, 0]], [[0, 1], [1, 0], [0, 0]]) == []
    # nobody's request fits: all three wait for ever
    assert d([0, 0], [[1, 0], [0, 1], [0, 0]], [[0, 1], [1, 0], [1, 0]]) == [0, 1, 2]
    assert d([1, 0], [[1, 0], [0, 1], [0, 0]], [[0, 1], [1, 0], [1, 0]]) == []
    # the solution's example: P2 finishes, P0 and P1 each wait for a second unit
    assert d([1, 0], [[1, 0], [1, 0], [0, 2]], [[2, 0], [2, 0], [0, 0]]) == [0, 1]


def test_monitor_semantics_and_exercise_5():
    script = ["C1", "P", "C2", "C1"]
    assert monitor_sim.run(script, hoare=False, use_while=False)[-1].endswith("!")
    assert not any(e.endswith("!") for h in (True, False)
                   for e in monitor_sim.run(script, h, True))
    assert not any(e.endswith("!") for e in monitor_sim.run(script, True, False))
    spurious = ["C1", "~C1", "C1"]
    for hoare in (True, False):
        assert monitor_sim.run(spurious, hoare, False)[-1].endswith("!")
        assert monitor_sim.run(spurious, hoare, True) == ["C1 waits", "C1 waits"]


def test_aba():
    s = aba_replay.Stack(["A", "B", "C"], tagged=False)
    seen, second = s.read(), s.next["A"]
    a, _ = s.pop(), s.pop()
    s.push(a)
    assert s.cas(seen, second) and s.contents() == "B -> C"
    t = aba_replay.Stack(["A", "B", "C"], tagged=True)
    seen, second = t.read(), t.next["A"]
    a, _ = t.pop(), t.pop()
    t.push(a)
    assert not t.cas(seen, second) and t.pop() == "A" and t.contents() == "C"


def test_linearizable_histories_and_exercise_9():
    h = linearizable.linearise
    assert h([("A", "enq", 1, None, 0, 2), ("B", "enq", 2, None, 3, 5),
              ("A", "deq", None, 2, 6, 8)]) is None
    assert h([("A", "enq", 1, None, 0, 4), ("B", "enq", 2, None, 1, 3),
              ("A", "deq", None, 2, 5, 6), ("B", "deq", None, 1, 7, 8)]) is not None
    # exercise 9: (a) linearisable, (b) not
    a = [("A", "enq", 1, None, 0, 10), ("B", "deq", None, 1, 1, 3),
         ("B", "deq", None, 2, 4, 6), ("C", "enq", 2, None, 2, 5)]
    order = h(a)
    assert [(t, op) for t, op, *_ in order] == [("A", "enq"), ("B", "deq"),
                                               ("C", "enq"), ("B", "deq")]
    b = [("A", "enq", 1, None, 0, 1), ("B", "enq", 2, None, 2, 3),
         ("C", "deq", None, 2, 4, 5), ("D", "deq", None, 1, 6, 7)]
    assert h(b) is None
