"""hoare_check.py -- check a Hoare-logic derivation step by step. A derivation is a
tree of rule applications; each node yields its triple {P} S {Q}, and the implications
of the rule of consequence are checked by the bit-blasting solver."""

import ast

from bitblast import check
from whilelang import parse
from wp import Substitute, conj, implies


def formula(text):
    return ast.parse(text, mode="eval").body


def same(a, b):
    return ast.dump(a) == ast.dump(b)


def derive(d, depth=0):
    """Return the triple (P, statements, Q) proved by derivation d, or raise."""
    rule, *args = d
    match rule:
        case "assign":  # {Q[e/x]} x = e {Q}
            source, q = args
            [s] = parse(source)
            p = Substitute(s.targets[0].id, s.value).visit(formula(q))
            triple = (p, [s], formula(q))
        case "seq":  # {P} S1 {R}, {R} S2 {Q}  gives  {P} S1; S2 {Q}
            p1, s1, r1 = derive(args[0], depth + 1)
            r2, s2, q2 = derive(args[1], depth + 1)
            assert same(r1, r2), "the middle assertions differ"
            triple = (p1, s1 + s2, q2)
        case "while":  # {I and b} S {I}  gives  {I} while b: S {I and not b}
            test, inv, body = args
            p, s, q = derive(body, depth + 1)
            b, i = formula(test), formula(inv)
            assert same(p, conj(i, b)) and same(q, i), "not of the form {I and b} S {I}"
            loop = ast.While(test=b, body=s, orelse=[])
            triple = (i, [loop], conj(i, ast.UnaryOp(op=ast.Not(), operand=b)))
        case "conseq":  # P => P', {P'} S {Q'}, Q' => Q  gives  {P} S {Q}
            pre, post, inner = args
            p1, s, q1 = derive(inner, depth + 1)
            for a, b in ((formula(pre), p1), (q1, formula(post))):
                valid, cex, _ = check(implies(a, b))
                assert valid, f"{ast.unparse(a)} does not imply {ast.unparse(b)}: {cex}"
            triple = (formula(pre), s, formula(post))
    p, s, q = triple
    shown = " ".join(" ".join(ast.unparse(x).split()) for x in s)
    print(f"{'  ' * depth}{rule:<7} {{{ast.unparse(p)}}} {shown} {{{ast.unparse(q)}}}")
    return triple


if __name__ == "__main__":
    body = (
        "conseq",
        "x <= 10 and x < 10",
        "x <= 10",
        ("assign", "x = x + 1", "x <= 10"),
    )
    derive(("conseq", "x <= 10", "x == 10", ("while", "x < 10", "x <= 10", body)))
    try:
        derive(
            (
                "conseq",
                "x <= 10 and x < 10",
                "x <= 10",
                ("assign", "x = x + 2", "x <= 10"),
            )
        )
    except AssertionError as failure:
        print("rejected:", failure)
