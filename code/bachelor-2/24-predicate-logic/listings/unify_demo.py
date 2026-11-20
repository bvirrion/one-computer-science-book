"""unify_demo.py: four pairs of atoms given to Robinson's algorithm."""
from formulas import Fun, parse, show
from unify import unify, walk


def atom(text):  # P(t1, ..., tn), unified as the term with P as its symbol
    p = parse(text)
    return Fun(p.name, p.args)


for left, right in [("P(x, f(y))", "P(g(z), f(x))"), ("Q(x, x)", "Q(a, b)"),
                    ("R(x)", "R(f(x))"), ("S(x, h(y))", "S(h(z), x)")]:
    sigma = unify(atom(left), atom(right))
    if sigma is None:
        print(f"{left} and {right}: no unifier")
        continue
    pairs = ", ".join(f"{x} := {show(walk(sigma[x], sigma))}" for x in sorted(sigma))
    both = show(walk(atom(left), sigma))
    print(f"{left} and {right}: {{{pairs}}}; both become {both}")
