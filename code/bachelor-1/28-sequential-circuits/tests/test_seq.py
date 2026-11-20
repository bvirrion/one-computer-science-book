"""Latches and flip-flops gate by gate, counters, registers, the memory, Moore and
Mealy conversions on random machines, the circuits made from state diagrams, the
control unit against the shared simulator, and the exercises."""

import random
import sys
from itertools import product
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import detect_0110  # noqa: E402
import mod6  # noqa: E402
import vending  # noqa: E402
from counter import ripple, synchronous, values_between_edges  # noqa: E402
from d_flipflop import clock, simulate  # noqa: E402
from detector import MOORE, circuit_run, equations  # noqa: E402
from lock import as_circuit, detector  # noqa: E402
from lock import circuit_run as lock_run  # noqa: E402
from moore_mealy import Mealy, mealy_to_moore, moore_to_mealy, same_outputs  # noqa: E402
from ram import RAM  # noqa: E402
from seq import all_words, minimal_sop, sop_value  # noqa: E402
from shift import register_next, shift_next  # noqa: E402
from sr_latch import sr_latch  # noqa: E402
from toy_control import example_programs, run  # noqa: E402


def test_sr_latch_sets_resets_and_oscillates():
    n, v = sr_latch(), {"S": 0, "R": 0, "Q": 0, "Qn": 1}
    for s, r, q in [(1, 0, 1), (0, 0, 1), (0, 1, 0), (0, 0, 0)]:
        for _ in range(3):
            v = n.tick(v | {"S": s, "R": r})
        assert (v["Q"], v["Qn"]) == (q, 1 - q)
    for _ in range(3):
        v = n.tick(v | {"S": 1, "R": 1})
    seen = set()
    for _ in range(6):
        v = n.tick(v | {"S": 0, "R": 0})
        seen.add((v["Q"], v["Qn"]))
    assert seen == {(0, 0), (1, 1)}


def test_flip_flop_stores_d_at_each_rising_edge():
    rng = random.Random(28)
    clk = clock(400, 10)
    edges = [t for t in range(1, 400) if clk[t] and not clk[t - 1]]
    d, level = [], 0
    for t in range(400):  # D changes only away from the edges
        if all(abs(t - e) > 3 for e in edges) and rng.random() < 0.2:
            level = 1 - level
        d.append(level)
    q = simulate(clk, d)
    for e in edges:
        assert q[e + 5] == d[e]


def test_counters():
    assert [run_[-1] for run_ in values_between_edges(synchronous(16))] == [
        (c + 1) % 8 for c in range(16)]
    cycles = values_between_edges(ripple(16))
    assert [run_[-1] for run_ in cycles] == [(c + 1) % 8 for c in range(16)]
    assert all(len(run_) == 2 for run_ in values_between_edges(synchronous(8)))


def test_registers():
    q = [0, 0, 0, 0]
    assert register_next(q, [1, 1, 0, 1], 0) == q
    assert register_next(q, [1, 1, 0, 1], 1) == [1, 1, 0, 1]
    for b in [1, 0, 0, 1, 1]:
        q = shift_next(q, b)
    assert q == [1, 1, 0, 0]


def test_ram_against_a_list():
    rng, ram, ref = random.Random(5), RAM(), [0] * 16
    for _ in range(300):
        a, v = rng.randrange(16), rng.randrange(16)
        if rng.random() < 0.5:
            ram.write(a, v)
            ref[a] = v
        else:
            assert ram.read(a) == ref[a]


def test_conversions_on_random_machines():
    rng = random.Random(7)
    for _ in range(30):
        states = range(rng.randint(1, 4))
        m = Mealy(0, {(q, a): (rng.choice(states), rng.randint(0, 1))
                      for q in states for a in (0, 1)})
        moore = mealy_to_moore(m, (0, 1))
        assert same_outputs(m, moore, (0, 1), 7)
        assert same_outputs(m, moore_to_mealy(moore), (0, 1), 7)


def test_minimal_sop_is_the_function():
    rng = random.Random(3)
    for _ in range(40):
        ones = [m for m in range(16) if rng.random() < 0.4]
        terms = minimal_sop(ones, [], 4)
        for m in range(16):
            assert sop_value(terms, [m >> (3 - i) & 1 for i in range(4)]) == (m in ones)


def test_detector_and_lock_circuits():
    eqs = equations()
    assert all(circuit_run(eqs, w) == MOORE.run(w) for w in all_words((0, 1), 9))
    mealy = detector([1, 0, 1, 1])
    states = sorted({q for q, _ in mealy.delta}, key=len)
    code, eqs, z = as_circuit(states, lambda s, a: mealy.delta[s, a][0],
                              lambda s, a: mealy.delta[s, a][1], 2, True)
    assert all(lock_run(eqs, z, 2, True, w) == mealy.run(w) for w in all_words((0, 1), 9))
    assert len(mealy_to_moore(mealy, (0, 1)).out) == 5


def test_control_unit_against_the_simulator():
    programs = list(example_programs())
    assert len(programs) >= 10
    for _, mem, inputs in programs:
        run(mem, inputs)  # asserts after every instruction


def test_exercises():
    assert detect_0110.check(9)
    assert mod6.count(12) == [t % 6 for t in range(13)]
    assert vending.check(5)
    assert vending.machine(2, 2) == (0, 1, 1)
    assert all(vending.machine(c, k)[0] in range(3) for c, k in product(range(3), repeat=2))
