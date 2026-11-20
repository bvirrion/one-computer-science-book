"""vcgen.py -- verification conditions of an annotated program: every loop carries an
invariant, and may carry a variant for termination. The program is correct for
{pre} S {post} when every condition returned is valid."""

import ast
import copy

from whilelang import annotations, parse
from wp import Substitute, conj, implies, wp


def neg(b):
    return ast.UnaryOp(op=ast.Not(), operand=b)


def awp(statements, q, vcs):
    """Like wp, but a loop's precondition is its invariant, and the loop adds its
    own conditions to the list vcs."""
    for s in reversed(statements):
        if isinstance(s, ast.While):
            inv, var, body = annotations(s)
            vcs.append(("preserved", implies(conj(inv, s.test), awp(body, inv, vcs))))
            vcs.append(("exit", implies(conj(inv, neg(s.test)), q)))
            if var is not None:  # the variant decreases: V < v0 after the body
                v0 = ast.Name(id=f"v{len(vcs)}")
                smaller = ast.Compare(left=var, ops=[ast.Lt()], comparators=[v0])
                start = ast.Compare(
                    left=copy.deepcopy(var), ops=[ast.Eq()], comparators=[v0]
                )
                entered = conj(conj(inv, s.test), start)
                vcs.append(("variant", implies(entered, awp(body, smaller, vcs))))
            q = inv
        elif isinstance(s, ast.If) and not isinstance(s.test, ast.Call):
            yes, no = awp(s.body, q, vcs), awp(s.orelse, q, vcs)
            q = conj(implies(s.test, yes), implies(neg(s.test), no))
        elif isinstance(s, ast.If):  # unknown(): both branches
            q = conj(awp(s.body, q, vcs), awp(s.orelse, q, vcs))
        else:
            q = wp([s], q)
    return q


def vcgen(pre, source, post):
    vcs = []
    entry = awp(parse(source), ast.parse(post, mode="eval").body, vcs)
    return [("entry", implies(ast.parse(pre, mode="eval").body, entry))] + vcs


__all__ = ["Substitute", "vcgen"]
