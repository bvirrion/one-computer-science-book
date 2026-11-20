import importlib.util
import io
import math
import random
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


rng = random.Random(2026)


def test_binary_fraction_digits():
    bf = load("listings", "to_binary_fraction").binary_fraction
    assert bf(Fraction(3, 8), 4) == "0110"
    for _ in range(100):
        x = Fraction(rng.randint(0, 999), 1000)
        d = bf(x, 40)
        approx = sum(Fraction(int(c), 2 ** (i + 1)) for i, c in enumerate(d))
        assert 0 <= x - approx < Fraction(1, 2**40)


def test_float_fields_rebuild_value():
    fields = load("listings", "float_bits").fields
    for x in [0.1, 1.0, -2.5, 3.75, 1e-3, 123456.789]:
        s, e, f = fields(x)
        significand = 1 + Fraction(int(f, 2), 2**52)
        value = (-1) ** int(s) * significand * Fraction(2) ** (int(e, 2) - 1023)
        assert value == Fraction(x)


def test_toy_format_and_dat():
    toy = load("listings", "toy_float")
    assert len(toy.values) == 128
    assert toy.values[0] == Fraction(1, 8) and toy.values[-1] == 31
    fig = load("figures", "toy_float_points")
    lines = ["value exponent"] + [f"{v:.7f} {e}" for v, e in fig.rows()]
    assert fig.OUT.read_text() == "\n".join(lines) + "\n"


def test_exact_binary_ends_and_is_exact():
    eb = load("exercises", "exact_binary").exact_binary
    d = eb(0.1)
    assert len(d) == 55
    assert sum(Fraction(int(c), 2 ** (i + 1)) for i, c in enumerate(d)) == Fraction(0.1)
    assert eb(0.375) == "011"


def test_almost_equal_matches_isclose():
    ae = load("exercises", "almost_equal").almost_equal
    for _ in range(500):
        a = rng.uniform(-10, 10)
        b = a + rng.uniform(-1e-8, 1e-8)
        assert ae(a, b) == math.isclose(a, b)
    assert ae(1e-12, 0.0, abs_=1e-9) and not ae(1e-12, 0.0)


def test_accumulate():
    mod = load("exercises", "accumulate")
    acc, mul = mod.times_accumulated(30), mod.times_multiplied(30)
    ex = mod.times_exact(30)
    assert acc[2] != 0.3 and ex[2] == 0.3
    wrong_acc = sum(a != e for a, e in zip(acc, ex))
    assert wrong_acc > sum(m != e for m, e in zip(mul, ex))


def test_quadratic_stable_is_accurate():
    mod = load("exercises", "quadratic")
    b, c = 1e8, 1.0
    exact = -c / b  # to about 1e-16 relative
    assert abs(mod.small_root_stable(b, c) - exact) / abs(exact) < 1e-12
    assert abs(mod.small_root_naive(b, c) - exact) / abs(exact) > 1e-2


def test_nan_max():
    mod = load("exercises", "nan_max")
    nan = float("nan")
    assert math.isnan(mod.largest_buggy([nan, 3.0, 7.0]))
    assert mod.largest_buggy([3.0, nan, 7.0]) == 7.0
    assert mod.largest([nan, 3.0, 7.0]) == 7.0
    with pytest.raises(AssertionError):
        mod.largest([nan])


def test_clock_drift_matches_published_table():
    mod = load("exercises", "clock_drift")
    published = {1: 0.0034, 8: 0.0275, 20: 0.0687, 48: 0.1648, 72: 0.2472, 100: 0.3433}
    for hours, seconds in published.items():
        assert round(float(mod.drift(hours, 23)), 4) == seconds
    assert round(float(mod.drift(100, 24)), 4) == 0.1287
