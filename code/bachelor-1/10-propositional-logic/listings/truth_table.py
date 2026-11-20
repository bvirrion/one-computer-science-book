"""truth_table.py: the truth table of a formula, and its complete DNF."""

from evaluate import valuations, value
from formula import Var, variables


def truth_table(f):
    names = variables(f)
    rows = [" ".join(names) + " | " + str(f)]
    for v in valuations(names):
        bits = " ".join("TF"[not v[n]] for n in names)
        rows.append(f"{bits} | {'TF'[not value(f, v)]}")
    return rows


def complete_dnf(f):
    """One conjunction of literals per true row: the formula's complete DNF."""
    terms = []
    for v in valuations(variables(f)):
        if value(f, v):
            terms.append(" & ".join(n if v[n] else "~" + n for n in sorted(v)))
    return " | ".join(f"({t})" for t in terms) if terms else "false: no row is true"


if __name__ == "__main__":
    p, q, r = Var("p"), Var("q"), Var("r")
    f = (p >> q) & (q | r)
    print("\n".join(truth_table(f)))
    print("complete DNF:", complete_dnf(f))
