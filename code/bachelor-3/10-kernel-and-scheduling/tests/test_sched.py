"""Tests for chapter 10: the simulator's policies, the bounds proved in the text and the
exercises, and the RISC-V switch."""
import itertools
import random
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE.parent / "listings"), str(HERE.parent / "exercises")]
from ex6_aging import priority_run  # noqa: E402
from ex12_starve import srtf, stream  # noqa: E402
from sched import Job, fifo, shortest, simulate  # noqa: E402
from rv import Machine  # noqa: E402

SWITCH = (HERE.parent / "listings" / "switch.S").read_text()


def test_example_timelines():
    jobs = [Job("A", 0, 8), Job("B", 1, 4), Job("C", 2, 9), Job("D", 3, 5), Job("E", 6, 2)]
    assert simulate(jobs, shortest).averages(jobs) == (13.4, 7.8, 7.8)
    rr = simulate(jobs, fifo, quantum=3)
    assert [g[2] for g in rr.gantt] == list("ABCDAEBCDAC")


def test_exercise_1_round_robin_by_hand():
    jobs = [Job("P", 0, 5), Job("Q", 1, 3), Job("R", 2, 1)]
    r = simulate(jobs, fifo, quantum=2)
    assert r.gantt == [(0, 2, "P"), (2, 4, "Q"), (4, 5, "R"), (5, 7, "P"), (7, 8, "Q"), (8, 9, "P")]
    assert r.finish == {"R": 5, "Q": 8, "P": 9}


def test_sjf_is_optimal_when_all_arrive_together():  # exercise 7, by brute force
    rng = random.Random(1)
    for _ in range(200):
        bursts = [rng.randint(1, 9) for _ in range(rng.randint(2, 6))]
        jobs = [Job(f"J{i}", 0, b) for i, b in enumerate(bursts)]
        best = min(sum(sum(p[:k]) for k in range(len(p))) for p in itertools.permutations(bursts))
        assert simulate(jobs, shortest).averages(jobs)[1] * len(jobs) == best


def test_round_robin_response_bound():  # exercise 8: response <= (n - 1) q
    rng = random.Random(2)
    for _ in range(200):
        n, q = rng.randint(1, 8), rng.randint(1, 5)
        jobs = [Job(f"J{i}", 0, rng.randint(1, 12)) for i in range(n)]
        r = simulate(jobs, fifo, quantum=q)
        assert all(r.first[j.name] <= (n - 1) * q for j in jobs)


def test_stride_error_below_one_quantum():  # exercise 10
    import stride  # noqa: F401  (runs the script: its worst error is printed and checked here)
    assert stride.worst["stride"] < 1


def test_exercise_6_aging_lets_the_low_priority_job_run():
    jobs = [("low", 0, 3)] + [(f"h{k}", 3 * k, 3) for k in range(10)]
    prio = {"low": 9, **{f"h{k}": 1 for k in range(10)}}
    assert priority_run(jobs, prio, age=10**9)["low"] == 33  # no aging: last
    assert priority_run(jobs, prio, age=3)["low"] < 33


def test_exercise_12_starvation_and_its_fix():
    jobs = stream(100)
    assert srtf(jobs)["long"] == 220  # runs only after the whole stream: 200 + 20
    assert srtf(jobs, age=2)["long"] == 54


def run(src):
    m = Machine(src)
    m.run()
    return m


def test_switch_output_and_cost():  # exercise 9: 29 instructions per switch, 8 switches
    assert run(SWITCH).output_text == "A1\nB10\nA2\nB20\nA3\nB30\n"
    m = Machine(SWITCH)
    start = m.prog.symbols["switch"]
    seen = {"inside": 0, "calls": 0}

    def count(step):
        seen["inside"] += start <= step.pc < start + 4 * 29
        seen["calls"] += step.pc == start

    m.run(trace=count)
    assert seen == {"inside": 8 * 29, "calls": 8}


def test_exercise_4_b_first():
    m = run(SWITCH.replace("la   a1, ctx_a\n        call switch            # run A",
                           "la   a1, ctx_b\n        call switch            # run A"))
    assert m.output_text == "B10\nA1\nB20\nA2\nB30\nA3\nB40\n"


def test_switch_bug():
    m = run((HERE.parent / "listings" / "switch_bug.S").read_text())
    assert m.output_text == "A1\nB10\n"


def test_timer_kernel_interleaves(monkeypatch, capsys):
    monkeypatch.chdir(HERE.parent / "listings")
    runpy.run_path("timer.py")
    printed = capsys.readouterr().out.split()[1]
    assert sorted(printed) == ["a"] * 12 + ["b"] * 12 and "ab" in printed and "ba" in printed
