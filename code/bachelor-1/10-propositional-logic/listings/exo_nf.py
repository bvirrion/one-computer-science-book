"""exo_nf.py: exercise 4."""

from formula import Var
from normal_forms import cnf, dnf, nnf, show_sets, simplify

p, q, r = Var("p"), Var("q"), Var("r")
f = ~(p & (q | ~r))
print("formula:", f)
print("NNF:", nnf(f))
print("CNF:", show_sets(simplify(cnf(f)), "&", "|"))
print("DNF:", show_sets(simplify(dnf(f)), "|", "&"))
