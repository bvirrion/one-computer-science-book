import importlib.util
import io
import math
import random
import sys
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_fraction_invariant():
    F = load("listings", "fraction").Fraction
    rng = random.Random(3)
    for _ in range(500):
        a = F(rng.randint(-50, 50), rng.choice([-1, 1]) * rng.randint(1, 50))
        b = F(rng.randint(-50, 50), rng.randint(1, 50))
        for c in (a + b, a * b):
            assert c.denominator() > 0
            assert math.gcd(c.numerator(), c.denominator()) == 1
        assert (a < b) == (float(a) < float(b)) or float(a) == float(b)


def test_dates_against_datetime():
    D = load("listings", "date_class").Date
    ex = load("exercises", "classes_ex")
    d = date(1999, 12, 25)
    for _ in range(1200):
        mine = D(d.year, d.month, d.day)
        nxt = d + timedelta(days=1)
        assert str(mine.next_day()) == nxt.isoformat()
        assert str(ex.previous_day(D(nxt.year, nxt.month, nxt.day))) == d.isoformat()
        d = nxt


def test_listing_results(monkeypatch):
    monkeypatch.chdir(HERE / "listings")
    assert load("listings", "paradigms").total == 1371
    h = load("listings", "harmonic")
    assert str(sum((h.Fraction(1, k) for k in range(1, 11)), h.Fraction(0))) == "7381/2520"


def test_exercises():
    ex = load("exercises", "classes_ex")
    t = ex.Tally()
    t.add()
    t.add(4)
    assert t.value() == 5
    F = ex.Fraction
    assert ex.sub(F(1, 2), F(1, 3)) == F(1, 6)
    assert ex.sum_even_squares(range(7)) == 56
    s = ex.Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2 and s.peek() == 1 and len(s) == 1 and not s.is_empty()
    a, b = ex.Basket(), ex.Basket()
    a.add(1)
    assert b.items == [1]
    a, b = ex.BasketFixed(), ex.BasketFixed()
    a.add(1)
    assert b.items == []
    p = ex.Polynomial([1, 1]) * ex.Polynomial([1, 1]) + ex.Polynomial([0, 0, -1])
    assert p.c == [1, 2] and p(3) == 7
