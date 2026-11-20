"""evaluate.py: the truth value of a formula under a valuation."""

from itertools import product

from formula import Bin, Not, Var, variables

TABLES = {"&": lambda a, b: a and b, "|": lambda a, b: a or b,
          "->": lambda a, b: (not a) or b, "<->": lambda a, b: a == b}


def value(f, v):
    """v maps each variable name of f to True or False."""
    match f:
        case Var(name):
            return v[name]
        case Not(sub):
            return not value(sub, v)
        case Bin(op, left, right):
            return TABLES[op](value(left, v), value(right, v))


def valuations(names):
    """All 2**len(names) valuations of the names, in the order of a truth table."""
    for bits in product([False, True], repeat=len(names)):
        yield dict(zip(names, bits))


def models(f):
    return [v for v in valuations(variables(f)) if value(f, v)]


def is_tautology(f):
    return len(models(f)) == 2 ** len(variables(f))


def is_satisfiable(f):
    return any(value(f, v) for v in valuations(variables(f)))


if __name__ == "__main__":
    p, q, r = Var("p"), Var("q"), Var("r")
    f = (p >> q) & ~(q | r)
    print(f, "under p=F q=F r=F:", value(f, {"p": False, "q": False, "r": False}))
    print(f, "under p=T q=F r=F:", value(f, {"p": True, "q": False, "r": False}))
    print("models of", f, ":", models(f))
    for g in [p | ~p, p & ~p, (p >> q) | (q >> p), ((p >> q) >> p) >> p, p >> (p & q)]:
        print(f"{str(g):24} tautology {is_tautology(g)!s:5}",
              f" satisfiable {is_satisfiable(g)}")
