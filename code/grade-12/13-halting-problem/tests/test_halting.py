import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_repeat_detector_agrees_with_running():
    rd = load("listings", "repeat_detector")
    pr = load("listings", "programs")
    hw = load("listings", "halts_within")
    for text, halts in [(pr.COUNTDOWN, True), (pr.FOREVER, False), (pr.WRAP, True),
                        (pr.SPIN, False)]:
        assert (rd.decide(text)[0] == "halts") == halts
        assert hw.halts_within(text, 10_000)[0] == halts


def test_random_programs_decided():
    rd = load("listings", "repeat_detector")
    hw = load("listings", "halts_within")
    rng = random.Random(5)
    ops = ["ADDI R0, 1", "ADDI R1, 3", "SUB R0, R1", "JNZ 0", "JZ 2", "JMP 4", "NOP",
           "ADD R1, R0", "SHL R0", "SHR R1", "XOR R0, R1"]
    for _ in range(200):
        lines = [rng.choice(ops) for _ in range(rng.randint(1, 6))] + ["HALT"]
        text = "\n".join(lines)
        verdict, steps, _ = rd.decide(text)
        if verdict == "halts":
            assert hw.halts_within(text, steps)[0]
        else:
            assert not hw.halts_within(text, 20_000)[0]


def test_contrarian_defeats_each_candidate():
    tc = load("listings", "try_contrarian")
    ct = load("listings", "contrarian")
    ex = load("exercises", "hp_ex")
    for d in [tc.always_yes, tc.always_no, tc.no_endless_loop, ex.short_is_stopping]:
        c = ct.make_contrarian(d)
        claim = d(c, c)
        actual = tc.run_for(c, c, 20_000).startswith("stops")
        assert claim != actual


def test_exercises(tmp_path):
    ex = load("exercises", "hp_ex")
    pr = load("listings", "programs")
    hw = load("listings", "halts_within")
    assert hw.halts_within(pr.WRAP, 512) == (False, 512)
    assert hw.halts_within(pr.COUNTDOWN.replace("R0, 3", "R0, 5"), 100) == (True, 18)
    f = tmp_path / "two.py"
    f.write_text("def a():\n    def b():\n        pass\n\n\nclass C:\n    def m(self):\n"
                 "        pass\n")
    assert ex.count_functions(f) == 3
    assert ex.first_repeat(pr.SPIN) == (513, 512)
    assert ex.first_repeat(pr.FOREVER) == (1, 1)
    assert ex.first_repeat(pr.WRAP) is None
    assert all(ex.multiply(a, b) == a * b % 256 for a in range(0, 30, 7) for b in range(9))
    t = [[True, False, True], [True, True, True], [False, False, False]]
    flip = ex.diagonal_flip(t)
    assert all(flip != row for row in t)
    assert 8 * 16 + 2 * 8 + 4 + 1 == 149
    assert 8 * 262 + 3 == 2099


def test_problem_bound():
    import math
    exp = 2099 * math.log10(2)
    assert int(exp) == 631 and int(10 ** (exp - 631)) == 7
    years = exp - 9 - math.log10(365.25 * 24 * 3600)
    assert int(years) == 615 and int(10 ** (years - 615)) == 2
    assert 2**149 // 10**44 == 7
