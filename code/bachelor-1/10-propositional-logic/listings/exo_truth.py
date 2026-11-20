"""exo_truth.py: exercises 1 to 3."""

from evaluate import is_satisfiable, is_tautology, value
from formula import Var, height, size, subformulas

p, q, r = Var("p"), Var("q"), Var("r")
f = ~(p & q) >> (r | ~p)
print("1.", f, "under p=T q=F r=F:", value(f, {"p": True, "q": False, "r": False}))
g = ((p | ~q) >> r) & ~~p
print("2.", g, "size", size(g), "height", height(g), "subformulas", len(subformulas(g)))
for h in [(p >> q) >> (~q >> ~p), (p >> q) >> (q >> p), p | (p >> q), ~(p >> (q >> p))]:
    kind = ("tautology" if is_tautology(h) else
            "satisfiable" if is_satisfiable(h) else "antilogy")
    print("3.", h, ":", kind)
