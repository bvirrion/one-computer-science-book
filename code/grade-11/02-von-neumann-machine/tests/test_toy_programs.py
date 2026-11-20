import math
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE.parents[1] / "shared" / "toymachine"))
from toymachine import Machine, ToyError, assemble  # noqa: E402


def run(folder, name, inputs=(), max_steps=10000):
    m = Machine(assemble((HERE / folder / name).read_text()), inputs=list(inputs))
    m.run(max_steps=max_steps)
    return m


def test_listings():
    assert run("listings", "max2.toy", [57, 201]).outputs == [201]
    assert run("listings", "max2.toy", [201, 57]).outputs == [201]
    assert run("listings", "sum_array.toy").outputs == [84]
    assert run("listings", "abs_value.toy", [214]).outputs == [42]  # -42 is stored as 214
    assert run("listings", "abs_value.toy", [42]).outputs == [42]
    assert run("listings", "multiply.toy", [13, 11]).outputs == [143]
    assert run("listings", "multiply.toy", [13, 0]).outputs == [0]
    assert run("listings", "call_square.toy").outputs == [9]


def test_exercises():
    rng = random.Random(2)
    for _ in range(50):
        xs = [rng.randrange(256) for _ in range(3)]
        assert run("exercises", "max3.toy", xs).outputs == [max(xs)]
    assert run("exercises", "max_array.toy").outputs == [130]
    try:
        run("exercises", "count_by_two.toy")
        raise AssertionError("expected no HALT")
    except ToyError:
        pass
    assert run("exercises", "count_by_two_fixed.toy").outputs == [7, 5, 3, 1]
    for n in (1, 5, 20):
        m = run("exercises", "sum.toy", [n])
        assert m.outputs == [n * (n + 1) // 2 % 256] and m.steps == 3 * n + 5
    for a in range(0, 256, 7):
        for b in range(1, 256, 11):
            assert run("exercises", "divide.toy", [a, b]).outputs == [a // b, a % b]
        for b in range(1, 256, 13):
            if a:
                assert run("exercises", "gcd.toy", [a, b]).outputs == [math.gcd(a, b)]
    for x in (0, 7, 25, 26, 200):
        assert run("exercises", "times_ten.toy", [x]).outputs == [10 * x % 256]
    for a, b in [(13, 11), (255, 255), (0, 9), (7, 0)]:
        assert run("listings", "shift_multiply.toy", [a, b]).outputs == [a * b % 256]


def test_bad_return_goes_wrong():
    m = Machine(assemble((HERE / "exercises" / "bad_return.toy").read_text()))
    pcs = []
    while not m.halted:
        pcs.append(m.pc)
        m.step()
    assert pcs[-1] == 40 and m.outputs == []  # RET jumped to R2's 40, an empty cell: HALT


def test_step_counts_script():
    env = {"PYTHONPATH": str(HERE.parents[1] / "shared" / "toymachine")}
    out = subprocess.run([sys.executable, str(HERE / "listings" / "step_counts.py")],
                         capture_output=True, text=True, check=True, env=env).stdout
    assert "worst 773 (first at b = 255), mean 390.5" in out
    assert "worst 63 (first at b = 128), mean 56.0" in out
