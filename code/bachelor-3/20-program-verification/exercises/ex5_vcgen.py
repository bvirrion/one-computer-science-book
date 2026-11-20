"""ex5_vcgen.py -- a verification-condition generator that forgets the condition at the
exit of a loop. Find a wrong program it accepts, and fix it."""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from vcgen import neg  # noqa: E402
from whilelang import annotations, parse  # noqa: E402
from wp import conj, implies, wp  # noqa: E402


def buggy_awp(statements, q, vcs):
    for s in reversed(statements):
        if isinstance(s, ast.While):
            inv, _, body = annotations(s)
            vcs.append(
                ("preserved", implies(conj(inv, s.test), buggy_awp(body, inv, vcs)))
            )
            q = inv  # BUG: nothing says that the invariant and the exit give q
        else:
            q = wp([s], q)
    return q


def fixed_awp(statements, q, vcs):
    for s in reversed(statements):
        if isinstance(s, ast.While):
            inv, _, body = annotations(s)
            vcs.append(
                ("preserved", implies(conj(inv, s.test), fixed_awp(body, inv, vcs)))
            )
            vcs.append(("exit", implies(conj(inv, neg(s.test)), q)))
            q = inv
        else:
            q = wp([s], q)
    return q


def vcgen_with(awp, pre, source, post):
    vcs = []
    entry = awp(parse(source), ast.parse(post, mode="eval").body, vcs)
    return [("entry", implies(ast.parse(pre, mode="eval").body, entry))] + vcs
