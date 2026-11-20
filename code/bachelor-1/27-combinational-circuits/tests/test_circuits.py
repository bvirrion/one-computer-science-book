"""The simulator, canonical forms, prime implicants against brute force, NAND
translations, adders and the ALU exhaustively, the NAND search, and the exercises."""

import random
import sys
from itertools import product
from pathlib import Path

import pytest

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from adders import correct, lookahead, ripple  # noqa: E402
from alu import OPS, alu, expected, run  # noqa: E402
from canonical import product_of_sums, sum_of_products  # noqa: E402
from circuit import Circuit, bits  # noqa: E402
from compare import less_than  # noqa: E402
from karnaugh import covers, essential, prime_implicants  # noqa: E402
from min_nand import search  # noqa: E402
from monotone import monotone_count  # noqa: E402
from multiplier import multiplier  # noqa: E402
from mux import mux4  # noqa: E402
from nand_only import nand_or, nand_xor  # noqa: E402
from seven_segment import DONT_CARE, SEGMENTS, cover  # noqa: E402


def evaluate_expression(expr, names, row):
    """Evaluate 'ab'c + ...' or '(a + b')(...)' on a row of 0/1 values."""
    env = dict(zip(names, row))

    def lit(tok):
        return 1 - env[tok[0]] if tok.endswith("'") else env[tok[0]]

    if expr.startswith("("):
        factors = expr[1:-1].split(")(")
        return int(all(any(lit(t) for t in f.split(" + ")) for f in factors))
    terms = expr.split(" + ")
    return int(any(all(lit(t) for t in split_literals(term)) for term in terms))


def split_literals(term):
    out = []
    for ch in term:
        if ch == "'":
            out[-1] += "'"
        else:
            out.append(ch)
    return out


def test_canonical_forms():
    rng = random.Random(27)
    for _ in range(50):
        table = {row: rng.randint(0, 1) for row in product((0, 1), repeat=3)}
        if 0 < sum(table.values()) < 8:
            def f(*r, table=table):
                return table[r]
            for form in (sum_of_products(f, "abc"), product_of_sums(f, "abc")):
                assert all(evaluate_expression(form, "abc", r) == table[r] for r in table)


def test_prime_implicants_against_brute_force():
    rng = random.Random(4)
    all_terms = ["".join(t) for t in product("01-", repeat=4)]
    for _ in range(100):
        ones = [m for m in range(16) if rng.random() < 0.4]
        dc = [m for m in range(16) if m not in ones and rng.random() < 0.15]
        allowed = set(ones) | set(dc)
        implicants = [t for t in all_terms
                      if all(m in allowed for m in range(16) if covers(t, m))
                      and any(covers(t, m) for m in ones)]

        def inside(s, t):  # every cell of s is a cell of t
            return all(b == "-" or a == b for a, b in zip(s, t))

        primes = sorted(t for t in implicants
                        if not any(u != t and inside(t, u) for u in implicants))
        got = [p for p in prime_implicants(ones, dc) if any(covers(p, m) for m in ones)]
        assert got == primes
        for e in essential(got, ones):
            assert any([p for p in got if covers(p, m)] == [e] for m in ones)


def test_seven_segment():
    for ones in SEGMENTS.values():
        terms = cover(ones, DONT_CARE)
        assert all(any(covers(t, d) for t in terms) == (d in ones) for d in range(10))


def test_nand_and_adders():
    for build, spec in ((nand_or, lambda x, y: x | y), (nand_xor, lambda x, y: x ^ y)):
        c = Circuit("x", "y")
        c.outputs["o"] = build(c, "x", "y")
        assert all(c.evaluate({"x": x, "y": y})["o"] == spec(x, y)
                   for x, y in product((0, 1), repeat=2))
    for n in (4, 8):
        assert correct(ripple(n), n) and correct(lookahead(n), n)
        assert ripple(n).delay() == 2 * n + 1
    assert lookahead(4).delay() == 4


def test_alu_and_search():
    c = alu()
    assert all(run(c, op, x, y) == expected(op, x, y)
               for op in OPS for x in range(16) for y in range(16))
    assert [search(k)[0] for k in range(1, 6)] == [3, 18, 180, 2700, 56700]
    assert search(4)[1] is None and search(5)[1] is not None


def to_inputs(x, y, n=4):
    return ({f"a{i}": v for i, v in enumerate(bits(x, n))}
            | {f"b{i}": v for i, v in enumerate(bits(y, n))})


@pytest.mark.parametrize("n", range(4))
def test_monotone(n):
    assert monotone_count(n) == [2, 3, 6, 20][n]


def test_exercises():
    m = mux4()
    for s1, s0, *xs in product((0, 1), repeat=6):
        values = {"s1": s1, "s0": s0} | {f"x{i}": v for i, v in enumerate(xs)}
        assert m.evaluate(values)["out"] == xs[2 * s1 + s0]
    lt, mul = less_than(), multiplier()
    for x in range(16):
        for y in range(16):
            assert lt.evaluate(to_inputs(x, y))["lt"] == int(x < y)
            out = mul.evaluate(to_inputs(x, y))
            assert sum(out[f"p{k}"] << k for k in range(8)) == x * y
