import math
import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import archive  # noqa: E402
import ex5_split  # noqa: E402
import ex6_delete  # noqa: E402
import ex11_linear  # noqa: E402
import ex12_workload  # noqa: E402
import pytest  # noqa: E402
from bptree import BPlusTree, bulk_load  # noqa: E402
from bufferpool import BufferPool  # noqa: E402
from extendible import Extendible  # noqa: E402
from lsm import LSM  # noqa: E402
from pagefile import PageFile  # noqa: E402
from slotted import SlottedPage  # noqa: E402

ops = st.lists(st.tuples(st.booleans(), st.integers(0, 80)), max_size=300)


def check_tree(t):
    """Sorted leaves chained in order, every non-root node at its minimum."""

    def walk(pid, lo, hi, depth, depths):
        n = t.nodes[pid]
        assert all(lo <= k < hi for k in n.keys) and n.keys == sorted(n.keys)
        if pid != t.root:
            assert not ex6_delete.too_small(t, n)
        if n.leaf:
            depths.add(depth)
            return
        assert len(n.kids) == len(n.keys) + 1 <= t.m
        bounds = [lo] + n.keys + [hi]
        for j, c in enumerate(n.kids):
            walk(c, bounds[j], bounds[j + 1], depth + 1, depths)

    depths = set()
    walk(t.root, -math.inf, math.inf, 1, depths)
    assert len(depths) == 1  # all leaves on one level


@settings(max_examples=150, deadline=None)
@given(st.integers(3, 7), ops)
def test_bptree_and_deletion_against_a_dict(m, script):
    t, ref = BPlusTree(m), {}
    for put, k in script:
        if put:
            t.insert(k, -k)
            ref[k] = -k
        else:
            ex6_delete.delete(t, k)
            ref.pop(k, None)
        check_tree(t)
    assert list(t.range(-1, 10**9)) == sorted(ref.items())
    assert all(t.search(k) == ref.get(k) for k in range(81))


@pytest.mark.parametrize("m", [3, 4, 5, 8, 255])
def test_height_bound(m):
    """h <= 2 + log_{ceil(m/2)}(n / (2 ceil((m-1)/2))), i.e. 1 + log_{m/2}(n/2) for even m."""
    rng = random.Random(m)
    for n in (10, 100, 1000, 20_000):
        t = BPlusTree(m)
        for k in rng.sample(range(10**6), n):
            t.insert(k, k)
        bound = 2 + math.log(n / (2 * math.ceil((m - 1) / 2)), math.ceil(m / 2))
        assert t.height() <= max(1, bound) + 1e-9


def test_bulk_load_valid_and_linear():
    for m in (3, 4, 7, 255):
        for n in (1, 2, 5, 99, 3000):
            t = bulk_load([(k, k) for k in range(n)], m)
            check_tree(t)
            assert list(t.range(0, n)) == [(k, k) for k in range(n)]
            assert t.writes == len(t.nodes) <= n / (m // 2) * 2 + 2  # O(n/m), no splits


def test_split_bug_loses_keys():
    b, f = ex5_split.Buggy(4), ex5_split.Fixed(4)
    for k in range(1, 11):
        b.insert(k, k)
        f.insert(k, k)
    assert [k for k in range(1, 11) if b.search(k) is None] == [3, 6, 9]
    assert all(f.search(k) == k for k in range(1, 11))


def test_slotted_page_keeps_record_identifiers():
    rng, page, ref = random.Random(5), SlottedPage(), {}
    for step in range(2000):
        if ref and rng.random() < 0.4:
            i = rng.choice(list(ref))
            page.delete(i)
            del ref[i]
        else:
            rec = bytes([step % 256]) * rng.randint(1, 60)
            i = page.insert(rec)
            if i is None:
                page.compact()
                i = page.insert(rec)
            if i is not None:
                assert i not in ref
                ref[i] = rec
        if step % 97 == 0:
            page.compact()
        assert all(page.get(i) == r for i, r in ref.items())
        count, start = page.header()
        assert page.free_space() == start - 4 - 4 * count >= 0


def test_buffer_pool_writes_back_and_respects_pins():
    f = PageFile()
    for _ in range(20):
        f.allocate()
    pool, rng, last = BufferPool(f, 4), random.Random(1), {}
    for step in range(3000):
        pid = rng.randrange(20)
        data = pool.fetch(pid)
        if rng.random() < 0.3:
            data[0] = step % 256
            last[pid] = step % 256
        pool.unpin(pid, dirty=pid in last and data[0] == last[pid])
    pool.flush()
    assert all(f.pages[p][0] == v for p, v in last.items())
    assert pool.hits + pool.misses == 3000
    for p in range(4):
        pool.fetch(p)  # four pinned frames
    with pytest.raises(RuntimeError):
        pool.fetch(10)


@settings(max_examples=60, deadline=None)
@given(st.lists(st.integers(0, 2**20), max_size=400), st.integers(1, 5))
def test_extendible_and_linear_against_a_dict(keys, cap):
    e, lin, ref = Extendible(cap), ex11_linear.LinearHash(cap=cap), {}
    for i, k in enumerate(keys):
        e.put(k, i)
        lin.put(k, i)
        ref[k] = i
    assert all(e.get(k) == v and lin.get(k) == v for k, v in ref.items())
    assert len(e.dir) == 2**e.depth
    assert all(b["depth"] <= e.depth and len(b["items"]) <= cap for b in e.dir)
    assert lin.size <= lin.max_load * cap * len(lin.buckets)


def test_lsm_against_a_dict_and_its_amplification():
    rng, ref = random.Random(8), {}
    t = LSM(memtable=50, ratio=4)
    for i in range(20_000):
        k = rng.randrange(5000)
        t.put(k, i)
        ref[k] = i
    assert all(t.get(k) == v for k, v in ref.items())
    assert all(t.get(k) is None for k in range(5000, 6000))
    L = len(t.levels)
    assert t.written / t.inserted <= L * (t.T + 2) / 2


def test_archive_heights_and_workloads():
    assert (archive.FANOUT, archive.LEAF) == (255, 254)
    assert [archive.height(10**e, 1.0) for e in (6, 9, 12)] == [3, 4, 5]
    for n in (1, 254, 255, 254 * 255, 254 * 255 + 1):
        assert bulk_load([(k, k) for k in range(n)], 255).height() == archive.height(
            n, 1.0
        )
    got = [ex12_workload.run(ex12_workload.workload(s)) for s in (0.9, 0.1)]
    assert [round(x, 2) for pair in got for x in pair] == [2.07, 0.72, 3.38, 0.13]


def test_ex4_plans_and_extendible_figure():
    import subprocess

    shared = HERE.parents[1] / "shared" / "sqlrun" / "sqlrun.py"
    out = subprocess.run(
        [sys.executable, str(shared), str(HERE / "exercises" / "ex4_plans.sql")],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    details = [
        line.split("|")[4].strip()
        for line in out.splitlines()
        if line.startswith("| ") and ("SCAN" in line or "SEARCH" in line)
    ]
    assert details == [
        "SEARCH loans USING COVERING INDEX loans_member (member_id=?)",
        "SEARCH loans USING COVERING INDEX loans_member (member_id>?)",
        "SCAN loans",
        "SEARCH loans USING INTEGER PRIMARY KEY (rowid=?)",
    ]
    e = Extendible(2, h=lambda k: k)  # the figure's directory doubling
    for k in (4, 9, 16, 1):
        e.put(k, k)
    assert e.depth == 1 and [sorted(b["items"]) for b in e.dir] == [[4, 16], [1, 9]]
    e.put(3, 3)
    assert e.depth == 2
    assert [(b["depth"], sorted(b["items"])) for b in e.dir] == [
        (1, [4, 16]),
        (2, [1, 9]),
        (1, [4, 16]),
        (2, [3]),
    ]
    assert e.dir[0] is e.dir[2]


def level_sizes(n, leaf, fan):
    sizes = [-(-n // leaf)]
    while sizes[-1] > 1:
        sizes.append(-(-sizes[-1] // fan))
    return sizes[::-1]


def test_problem_and_exercise_numbers():
    assert level_sizes(10**9, 254, 255) == [1, 61, 15_440, 3_937_008]
    assert level_sizes(10**6, 254, 255) == [1, 16, 3_938]
    assert len(level_sizes(10**12, 254, 255)) == 5
    assert len(level_sizes(10**9, 175, 175)) == 5
    assert 255**3 * 254 == 4_211_669_250
    assert len(level_sizes(10**7, 99, 100)) == 4  # ex 2, full nodes
    t = BPlusTree(255)  # increasing keys leave every leaf but the last half full
    for k in range(100_000):
        t.insert(k, k)
    leaves = [len(n.keys) for n in t.nodes if n.leaf]
    assert set(leaves[:-1]) == {127}
    page = SlottedPage()  # ex 1
    ids = [page.insert(bytes(40)) for _ in range(30)]
    assert page.free_space() == 2772
    for i in ids[:10]:
        page.delete(i)
    assert page.free_space() == 2772
    page.compact()
    assert page.free_space() == 3172
    more = 0
    while page.insert(bytes(40)) is not None:
        more += 1
    assert (more, page.free_space()) == (73, 0)
    f = PageFile()  # ex 3
    for _ in range(6):
        f.allocate()
    pool, seen = BufferPool(f, 3), []
    for pid in (1, 2, 3, 1, 4, 1, 5, 2):
        before = pool.hits
        pool.fetch(pid)
        pool.unpin(pid)
        seen.append(pool.hits > before)
    assert seen == [False, False, False, True, False, False, False, False]
