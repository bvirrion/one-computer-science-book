"""wp.py -- weakest preconditions of loop-free programs, formulas being expressions of
the while-language; implies(a, b) is implication."""

import ast
import copy

from whilelang import parse


class Substitute(ast.NodeTransformer):
    """Q[e/x]: replace every occurrence of the variable x by the expression e."""

    def __init__(self, x, e):
        self.x, self.e = x, e

    def visit_Name(self, node):
        return copy.deepcopy(self.e) if node.id == self.x else node


def conj(a, b):
    return ast.BoolOp(op=ast.And(), values=[a, b])


def implies(a, b):
    return ast.Call(func=ast.Name(id="implies"), args=[a, b], keywords=[])


def wp(statements, q):
    for s in reversed(statements):  # wp(S1; S2, Q) = wp(S1, wp(S2, Q))
        match s:
            case ast.Assign(targets=[ast.Name(id=x)], value=e):
                q = Substitute(x, e).visit(copy.deepcopy(q))
            case ast.If(
                test=ast.Call(func=ast.Name(id="unknown")), body=yes, orelse=no
            ):
                q = conj(wp(yes, q), wp(no, q))  # either branch may run
            case ast.If(test=b, body=yes, orelse=no):
                q = conj(
                    implies(b, wp(yes, q)),
                    implies(ast.UnaryOp(op=ast.Not(), operand=b), wp(no, q)),
                )
            case ast.Assert(test=b):
                q = conj(b, q)
            case ast.Pass():
                pass
            case _:
                raise ValueError("wp: loops need an invariant (see vcgen.py)")
    return q


if __name__ == "__main__":

    def show(program, post):
        pre = wp(parse(program), ast.parse(post, mode="eval").body)
        lines = (line.strip() for line in program.strip().splitlines())
        print(f"program: {' | '.join(lines)}")
        print(f"  wp for {post}:  {ast.unparse(pre)}")

    show("y = x + 1\nx = y + y", "x < 100")
    show("t = x\nx = y\ny = t", "x == a and y == b")
    show("if x < y:\n    m = y\nelse:\n    m = x", "m >= x")
