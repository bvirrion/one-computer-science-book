"""Hand-traced sequences, the chapter's propositions checked by simulation, the 3C split."""
import os
from pathlib import Path

import pytest
from blur_sim import N as BLUR_N
from blur_sim import read_misses
from cache import Cache
from flush import dirty_lines, total_writes
from three_c import classify

HERE = Path(__file__).resolve().parent.parent


def run(cache, addresses, writes=()):
    return ["H" if cache.access(a, a in writes) else "M" for a in addresses]


def test_fields():
    c = Cache(256, 16, 1)                          # 16 sets: 4 offset bits, 4 index bits
    assert c.split(0x1234) == (0x12, 0x3, 0x4)
    l1 = Cache(48 * 1024, 64, 12)                  # the laptop's L1: 64 sets
    assert (l1.sets, l1.offset_bits, l1.index_bits) == (64, 6, 6)


def test_hand_trace_direct_mapped():
    c = Cache(256, 16, 1)
    trace = [0x000, 0x004, 0x010, 0x100, 0x000, 0x110, 0x014, 0x200]
    assert run(c, trace) == list("MHMMMMMM")


def test_hand_trace_two_way():
    c = Cache(256, 16, 2)                          # 8 sets of 2
    trace = [0x000, 0x080, 0x000, 0x100, 0x080, 0x000, 0x100]
    assert run(c, trace) == list("MMHMMMM")
    assert [t for t in c.lines_in(0)] == [0, 2]    # tags, least recently used first


def test_write_policies():
    trace = [0x000, 0x004, 0x100, 0x000]
    wb = Cache(256, 16, 1, write_back=True)
    run(wb, trace, writes={0x004})
    assert (wb.memory_writes, dirty_lines(wb)) == (1, 0)   # the dirty line evicted by 0x100
    wt = Cache(256, 16, 1, write_back=False)
    run(wt, trace, writes={0x004})
    assert wt.memory_writes == 1
    wb2 = Cache(256, 16, 1)
    for _ in range(10):
        wb2.access(0x40, write=True)
    assert (wb2.memory_writes, dirty_lines(wb2), total_writes(wb2)) == (0, 1, 1)
    na = Cache(256, 16, 1, write_allocate=False)
    assert run(na, [0x20, 0x20], writes={0x20}) == ["M", "M"]


@pytest.mark.parametrize("lines", [4, 8, 32])
def test_cyclic_sweep(lines):
    c = Cache(16 * lines, 16, lines)               # fully associative, `lines` lines
    trace = [16 * (k % (lines + 1)) for k in range(10 * (lines + 1))]
    assert set(run(c, trace)) == {"M"}             # every access misses
    c2 = Cache(16 * lines, 16, lines)
    trace2 = [16 * (k % lines) for k in range(10 * lines)]
    assert run(c2, trace2).count("M") == lines     # one fewer line: only the first sweep


@pytest.mark.parametrize("n, line", [(32, 32), (64, 64), (16, 16)])
def test_traversal(n, line):
    rows = [4 * (i * n + j) for i in range(n) for j in range(n)]
    cols = [4 * (i * n + j) for j in range(n) for i in range(n)]
    c = Cache(1024, line, 1)
    assert sum(not c.access(a) for a in rows) == n * n * 4 // line
    c = Cache(1024, line, 1)
    if 4 * n * n > 1024 and n * line > 1024:       # a column needs more lines than fit
        assert sum(not c.access(a) for a in cols) == n * n


def test_three_c_adds_up():
    import random
    rng = random.Random(7)
    trace = [rng.randrange(0, 8192) & ~3 for _ in range(5000)]
    for ways in (1, 2, 4, 64):
        misses, c = classify(trace, 1024, 16, ways)
        assert misses == sum(c.values())
        assert c["compulsory"] == len({a // 16 for a in trace})


def test_matrix_sum_trace():
    from trace_demo import load_addresses
    os.chdir(HERE / "listings")
    for order, want in [(0, 128), (1, 1024)]:
        out, loads = load_addresses(order)
        c = Cache(1024, 32, 1)
        assert out == "31744" and sum(not c.access(a) for a in loads) == want


def test_blur_rows_one_in_sixteen():
    reads, m = read_misses("rows")
    assert m == BLUR_N * BLUR_N * 4 // 64          # every line of the image once
    # a strip of 16 columns touches 3 lines per row of the image, except at the two edges
    assert read_misses("strips", 16)[1] == 3 * (BLUR_N // 16) * BLUR_N - 2 * BLUR_N


@pytest.mark.parametrize("capacity, want", [(31, 1024), (32, 256), (64, 256)])
def test_traversal_fully_associative(capacity, want):
    n, line = 32, 16                               # 32 x 32 ints, 4 per line
    cols = [4 * (i * n + j) for j in range(n) for i in range(n)]
    c = Cache(capacity * line, line, capacity)
    assert sum(not c.access(a) for a in cols) == want   # n * n below n lines, else n * n / 4


def test_exercise_traces():
    ex1 = [0x00, 0x04, 0x08, 0x10, 0x80, 0x00, 0x14, 0x90, 0x1C, 0x84]
    assert "".join(run(Cache(128, 16, 1), ex1)) == "MHHMMMHMMM"
    ex5 = [0x000, 0x100, 0x000, 0x200, 0x100, 0x084, 0x000, 0x300, 0x004]
    two = Cache(256, 16, 2)
    assert "".join(run(two, ex5)) == "MMHMMMMMH" and two.lines_in(0) == [6, 0]
    assert "".join(run(Cache(256, 16, 1), ex5)) == "MMMMMMMMM"


def test_wrong_bits_and_amat():
    import runpy
    os.chdir(HERE / "listings")
    runpy.run_path("exo_wrong_bits.py")             # prints 16 and 32 misses
    amat = 1 + 0.05 * (3 + 0.2 * (16 + 0.3 * 130))
    assert abs(amat - 1.7) < 1e-9
