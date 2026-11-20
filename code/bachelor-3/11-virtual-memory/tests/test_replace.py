"""Tests for the replacement policies, the stack property, and exercises 3, 6, 8 and 11."""
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE.parent / "listings"), str(HERE.parent / "exercises")]

from ex6_clock_dirty import clock_dirty, clock_writes  # noqa: E402
from replace import clock, fifo, lru, opt  # noqa: E402
from table_size import table_bytes  # noqa: E402

BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def test_belady_anomaly():
    assert (fifo(BELADY, 3), fifo(BELADY, 4)) == (9, 10)
    assert (lru(BELADY, 3), lru(BELADY, 4)) == (10, 8)
    assert (opt(BELADY, 3), opt(BELADY, 4)) == (7, 6)


def test_opt_is_never_beaten():  # exercise 7, checked on random strings
    rng = random.Random(3)
    for _ in range(300):
        refs = [rng.randint(1, 7) for _ in range(rng.randint(1, 30))]
        f = rng.randint(1, 5)
        assert opt(refs, f) <= min(fifo(refs, f), lru(refs, f), clock(refs, f))


def lru_resident(refs, frames):
    resident = []
    for p in refs:
        if p in resident:
            resident.remove(p)
        resident.append(p)
        resident = resident[-frames:]
        yield set(resident)


def test_lru_is_a_stack_algorithm():  # exercise 10: inclusion at every step
    rng = random.Random(4)
    for _ in range(300):
        refs = [rng.randint(1, 8) for _ in range(30)]
        f = rng.randint(1, 6)
        for small, big in zip(lru_resident(refs, f), lru_resident(refs, f + 1)):
            assert small <= big
        assert lru(refs, f + 1) <= lru(refs, f)


def test_exercise_3_lru_by_hand():
    assert lru([7, 0, 1, 2, 0, 3, 0, 4, 2, 3], 3) == 8


def test_exercise_6_clock_with_dirty_bit():
    refs = [(1, "w"), (2, "r"), (3, "r"), (4, "r")]
    assert clock_dirty(refs, 3) == (4, 0)  # evicts the clean page 2
    assert clock_writes(refs, 3) == (4, 1)  # plain clock evicts the dirty page 1
    rng = random.Random(6)
    for _ in range(200):
        refs = [(rng.randint(1, 8), rng.choice("rw")) for _ in range(40)]
        faults, writes = clock_dirty(refs, 4)
        assert opt([p for p, _ in refs], 4) <= faults and writes <= faults


def test_exercise_8_table_pages():
    regions = [(0x00400000, 64 * 1024), (0x20000000, 8 << 20), (0x7FFF0000, 64 * 1024)]
    assert table_bytes(regions) == (16 + 2048 + 16, 4, 5 * 4096)


def cyclic_trap(frames, rounds):  # exercise 11: hot pages, then a new page each round
    hot = list(range(1, frames))
    refs = list(hot)
    for r in range(rounds):
        refs += [100 + r] + hot
    return refs


def test_exercise_11_clock_k_times_worse():
    for k in (2, 3, 5):
        refs = cyclic_trap(2 * k - 1, 200)
        assert lru(refs, 2 * k - 1) == 2 * k - 2 + 200
        assert clock(refs, 2 * k - 1) == 2 * k - 2 + 200 * k
