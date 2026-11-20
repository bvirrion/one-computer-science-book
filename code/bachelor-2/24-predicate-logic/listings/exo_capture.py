"""exo_capture.py: a substitution function, and three substitutions it makes."""
from formulas import Exists, Forall, Fun, Not, Pred, Var, parse, show


def replace(e, x, t):  # e[t/x]?
    match e:
        case Var(y):
            return t if y == x else e
        case Fun(f, args) | Pred(f, args):
            return type(e)(f, tuple(replace(a, x, t) for a in args))
        case Not(a):
            return Not(replace(a, x, t))
        case Forall(y, a) | Exists(y, a):
            return e if y == x else type(e)(y, replace(a, x, t))
    return type(e)(replace(e.left, x, t), replace(e.right, x, t))


for text, x, t in [("Friend(x, z) & exists y. Friend(x, y)", "z", "y"),
                   ("forall x. Friend(x, z)", "x", "y"),
                   ("exists y. Friend(x, y)", "x", "y")]:
    phi = parse(text)
    print(f"({text})[{t}/{x}] = {show(replace(phi, x, Var(t)))}")
