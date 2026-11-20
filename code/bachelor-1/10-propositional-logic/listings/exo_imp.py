"""exo_imp.py: exercise 5, an evaluator with a wrong implication."""

from evaluate import valuations
from formula import Bin, Not, Var

TABLES = {"&": lambda a, b: a and b, "|": lambda a, b: a or b,
          "->": lambda a, b: b if a else False,  # "if a then b"
          "<->": lambda a, b: a == b}


def value(f, v):
    match f:
        case Var(name):
            return v[name]
        case Not(sub):
            return not value(sub, v)
        case Bin(op, left, right):
            return TABLES[op](value(left, v), value(right, v))


p, q = Var("p"), Var("q")
for f in [p >> q, p >> p, (p >> q) | (q >> p)]:
    row = [value(f, v) for v in valuations(["p", "q"])]
    print(f"{str(f):20}", " ".join("TF"[not b] for b in row))
