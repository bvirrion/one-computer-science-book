"""Both integer square roots against math.isqrt, and the iteration counts."""

import math
import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))

from exo_mystery import mystery  # noqa: E402
from isqrt import isqrt_bisect, isqrt_newton  # noqa: E402


@given(st.integers(0, 2**64 - 1))
def test_isqrt(n):
    (r1, s1), (r2, s2) = isqrt_bisect(n), isqrt_newton(n)
    assert r1 == r2 == math.isqrt(n)
    assert s1 <= n.bit_length()  # n.bit_length() == ceil(log2(n + 1))
    assert s2 <= s1 or n < 4


def test_small():
    for n in range(2000):
        assert isqrt_bisect(n)[0] == isqrt_newton(n)[0] == math.isqrt(n)


@given(st.integers(-5, 5), st.integers(0, 40))
def test_mystery_is_power(x, n):
    assert mystery(x, n) == x ** n
