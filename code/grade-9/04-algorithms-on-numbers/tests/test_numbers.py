"""Grade 9, chapter 4: algorithms on numbers."""

import importlib.util
import io
import math
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

from gcd import gcd  # noqa: E402
from is_prime import is_prime  # noqa: E402
from sieve import sieve  # noqa: E402


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    out = io.StringIO()
    with redirect_stdout(out):
        spec.loader.exec_module(module)
    return module, out.getvalue()


def test_primes_agree():
    slow, _ = load("listings", "is_prime_slow")
    primes = sieve(2000)
    assert [n for n in range(2000) if is_prime(n)[0]] == primes
    assert [n for n in range(300) if slow.is_prime_slow(n)[0]] == sieve(300)
    assert len(sieve(100_000)) == 9592
    assert is_prime(1_000_003) == (True, 999) and math.isqrt(1_000_003) == 1000
    assert is_prime(10_007) == (True, 99)


def test_euclid():
    for a in range(1, 120):
        for b in range(1, 120):
            assert gcd(a, b)[0] == math.gcd(a, b)
            if b <= a:
                assert a % b < a / 2            # the proposition of the chapter
    sub, out = load("listings", "gcd_subtract")
    assert out.strip().endswith("gcd: 6")
    assert gcd(48, 18) == (6, 3)
    assert [gcd(13, 8)[1], gcd(21, 13)[1], gcd(100, 1)[1]] == [5, 6, 1]
    best = max((gcd(a, b)[1], a, b) for a in range(1, 1000) for b in range(1, a))
    assert best == (14, 987, 610)


def test_figures_data():
    subprocess.run([sys.executable, str(HERE / "figures" / "number_figures.py")],
                   check=True)
    primes = (HERE / "figures" / "out" / "primes.tex").read_text()
    assert primes.strip() == "\\def\\gnineprimes{" + ",".join(
        map(str, sieve(101))) + "}"


def test_exercises():
    _, out = load("exercises", "perfect")
    assert out.split() == ["6", "28", "496"]
    bug, _ = load("exercises", "is_prime_one_bug")
    fixed, _ = load("exercises", "is_prime_one_fixed")
    assert bug.is_prime(1) and not fixed.is_prime(1) and not fixed.is_prime(0)
    square, _ = load("exercises", "square_bug")
    assert square.is_prime(49) and square.is_prime(25) and square.is_prime(4)
    assert not square.is_prime(6)
    _, out = load("exercises", "gcd3")
    assert out.strip() == "42"
    _, out = load("exercises", "twins")
    assert out.strip() == "35 pairs; the last: [881, 883]"
    nxt, _ = load("exercises", "next_prime")
    assert nxt.next_prime(1000) == (1009, 76)
    assert nxt.next_prime(1) == (2, 0) and nxt.next_prime(13)[0] == 17
