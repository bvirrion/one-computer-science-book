"""exo_free.py: the free variables of five formulas."""
from formulas import free, parse

for text in ["forall x. R(x, y)",
             "(forall x. P(x)) -> P(x)",
             "exists x. forall y. R(x, y) & R(y, z)",
             "forall x. (exists x. P(x)) -> Q(x, f(y))",
             "exists y. y = f(x) & forall x. ~R(x, y)"]:
    print(f"{text:45} free: {sorted(free(parse(text)))}")
