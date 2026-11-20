"""exo_cnf_bug.py: exercise 6, a CNF converter that does not distribute."""

from evaluate import valuations, value
from formula import Bin, Var
from normal_forms import literal, nnf, show_sets


def literals(g):
    if isinstance(g, Bin):
        return literals(g.left) | literals(g.right)
    return frozenset([literal(g)])


def cnf_wrong(f):
    g = nnf(f)
    if isinstance(g, Bin) and g.op == "&":
        return cnf_wrong(g.left) + cnf_wrong(g.right)
    return [literals(g)]  # a disjunction: all its literals in one clause


def holds(clauses, v):
    return all(any(v[x] if not x.startswith("~") else not v[x[1:]] for x in c)
               for c in clauses)


p, q, r = Var("p"), Var("q"), Var("r")
f = p | (q & r)
print("formula:", f, " CNF given:", show_sets(cnf_wrong(f), "&", "|"))
for v in valuations(["p", "q", "r"]):
    if value(f, v) != holds(cnf_wrong(f), v):
        print("differ at", v)
