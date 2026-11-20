"""exo_unify.py: four more pairs of atoms given to unify."""
from formulas import Fun, parse, show
from unify import unify, walk


def atom(text):
    p = parse(text)
    return Fun(p.name, p.args)


for left, right in [("P(f(x), y)", "P(y, f(a))"), ("P(x, f(x))", "P(f(y), y)"),
                    ("P(x, y, z)", "P(y, z, a)"), ("P(g(x), x)", "P(f(y), a)")]:
    sigma = unify(atom(left), atom(right))
    if sigma is None:
        print(f"{left} and {right}: no unifier")
    else:
        both = show(walk(atom(left), sigma))
        print(f"{left} and {right}: both become {both}")
