"""ex6_for.py -- the rule for a counted loop, for i in range(a, b) with a <= b, the body
not assigning i, a, b:
    {I and a <= i and i < b} body {I[i + 1 / i]}
    -------------------------------------------------
    {I[a / i]} for i in range(a, b): body {I[b / i]}
for_vcs returns the conditions for {pre} for ... {post}, with invariant I."""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from whilelang import parse  # noqa: E402
from wp import Substitute, conj, implies, wp  # noqa: E402


def f(text):
    return ast.parse(text, mode="eval").body


def for_vcs(pre, i, a, b, inv, body, post):
    def at(e):
        return Substitute(i, f(e)).visit(f(inv))

    inside = conj(conj(f(inv), f(f"{a} <= {i}")), f(f"{i} < {b}"))
    return [
        ("entry", implies(f(pre), conj(at(a), f(f"{a} <= {b}")))),
        ("preserved", implies(inside, wp(parse(body), at(f"{i} + 1")))),
        ("exit", implies(at(b), f(post))),
    ]
