import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import brent  # noqa: E402
import ex5_interleave  # noqa: E402
import ex9_overhead  # noqa: E402
import workspan  # noqa: E402


def test_work_and_span_formulas():
    for k in range(1, 11):
        n = 2**k
        assert workspan.work_span(workspan.reduction(n)) == (n - 1, k)
        assert workspan.work_span(workspan.hillis_steele(n)) == (n * k - (n - 1), k)
        assert workspan.work_span(workspan.blelloch(n)) == (
            2 * (n - 1),
            max(1, 2 * k - 1),
        )
        assert workspan.work_span(workspan.merge_sort(n)[0]) == (n * k, 2 * n - 2)


@settings(max_examples=60, deadline=None)
@given(
    st.integers(20, 400), st.integers(1, 15), st.integers(0, 10**6), st.integers(1, 9)
)
def test_greedy_within_brent(n, width, seed, p):
    dag = brent.random_dag(n, width, seed)
    w, s = workspan.work_span(dag)
    t = brent.greedy(dag, p)
    assert max(math.ceil(w / p), s) <= t <= w / p + s  # hence t < 2 * lower bound


def test_brent_listing_numbers():
    dag = workspan.merge_sort(256)[0]
    w, s = workspan.work_span(dag)
    assert (w, s) == (2048, 510)
    assert brent.greedy(dag, 4) == 768 and brent.greedy(dag, 8) == 608


def test_exercise_4_vectorised_loops(tmp_path):
    shutil.copy(HERE / "exercises" / "ex4_loops.c", tmp_path)
    out = subprocess.run(
        ["gcc", "-O3", "-fopt-info-vec-optimized", "-c", "ex4_loops.c"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    lines = {int(x.split(":")[1]) for x in out.splitlines() if "loop vectorized" in x}
    assert lines == {4, 10}  # (a) and (b); not (c), line 16


def test_exercise_5_lost_update(capsys):
    assert (
        ex5_interleave.run(([5, 7], [3, 4]), [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]) == 14
    )
    for _ in range(200):  # any script that runs each += whole gives the right sum
        parts = (
            [random.randint(1, 9) for _ in range(3)],
            [random.randint(1, 9) for _ in range(3)],
        )
        order = random.sample([0] * 3 + [1] * 3, 6)
        script = [t for t in order for _ in range(3)]
        assert ex5_interleave.run(parts, script) == sum(parts[0]) + sum(parts[1])


def test_exercise_9():
    assert ex9_overhead.best(0.05, 0.001) == 31
    assert round(1 / ex9_overhead.time(31, 0.05, 0.001), 2) == 8.96
    assert ex9_overhead.best(0.05, 0.0001) == 97


def test_solution_numbers():
    amdahl = lambda f, p: 1 / (f + (1 - f) / p)  # noqa: E731
    assert round(amdahl(0.1, 8), 3) == 4.706 and abs(amdahl(1 / 21, 8) - 6) < 1e-9
    gustafson = lambda f, p: f + (1 - f) * p  # noqa: E731
    assert round(gustafson(0.1, 8), 1) == 7.3
    n = 2**24  # psort model: T_p = (n/p) log2(n/p) + 2n(1 - 1/p), T_1 = n log2 n
    t = lambda p: n / p * math.log2(n / p) + 2 * n * (1 - 1 / p)  # noqa: E731
    assert [round(t(1) / t(p), 2) for p in (2, 4, 8)] == [1.92, 3.43, 5.49]
    assert (
        round(n / (2 * n / 8 + 2 * 24), 3) == 4.0
    )  # scan: Brent on 8 against n additions


def test_problem_and_scan_numbers():
    n = 2**20  # exercise 7: Brent's bound on 8 processors for both scans
    hs = (n * 20 - (n - 1)) / 8 + 20
    bl = 2 * (n - 1) / 8 + 40
    assert (round(hs), round(bl), round(hs / bl, 1)) == (2490388, 262184, 9.5)
    n = 2**24  # the weekend problem
    w, s = workspan.work_span(workspan.blelloch(2**10))
    assert (w, s) == (2 * (2**10 - 1), 19)  # span 2k - 1
    assert 2 * (n - 1) == 33_554_430 and round(2 * (n - 1) / 47) == 713_924
    assert n * 24 - (n - 1) == 385_875_969
    assert [round(n / (2 * (n - 1) / p + 47), 2) for p in (1, 2, 4, 8)] == [
        0.5,
        1.0,
        2.0,
        4.0,
    ]
    assert round(n / (2 * n / 1000 + 47), 1) == 499.3
    assert sum([0, 62, 0, 29, 8, 34, 0]) == 133
