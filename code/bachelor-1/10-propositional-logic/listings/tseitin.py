"""tseitin.py: an equisatisfiable CNF, one new variable per binary connective."""

from formula import Bin, Not, Var
from quine import neg

GATES = {  # the clauses of t <-> (a op b)
    "&": lambda t, a, b: [[neg(t), a], [neg(t), b], [t, neg(a), neg(b)]],
    "|": lambda t, a, b: [[neg(t), a, b], [t, neg(a)], [t, neg(b)]],
    "->": lambda t, a, b: [[neg(t), neg(a), b], [t, a], [t, neg(b)]],
    "<->": lambda t, a, b: [[neg(t), neg(a), b], [neg(t), a, neg(b)],
                            [t, a, b], [t, neg(a), neg(b)]],
}


def tseitin(f, prefix="t"):
    clauses, names = [], {}

    def literal(g):
        """A literal that is true exactly when g is, given the gate clauses."""
        match g:
            case Var(name):
                return name
            case Not(sub):
                return neg(literal(sub))
            case Bin(op, left, right):
                if g not in names:  # equal subformulas share one variable
                    a, b = literal(left), literal(right)
                    names[g] = t = f"{prefix}{len(names) + 1}"
                    clauses.extend(frozenset(c) for c in GATES[op](t, a, b))
                return names[g]

    clauses.append(frozenset([literal(f)]))  # and the formula itself is true
    return clauses
