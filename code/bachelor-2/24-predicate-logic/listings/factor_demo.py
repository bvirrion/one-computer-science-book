"""factor_demo.py: two clauses with no model, refuted only once factoring is allowed."""
from formulas import Fun, Pred, Var, free, show
from unify import factors, resolvents


def once(t, tau):
    """t with every variable replaced at the same time, once."""
    match t:
        case Var(v):
            return tau.get(v, t)
        case Fun(f, args):
            return Fun(f, tuple(once(a, tau) for a in args))


def normal(c):
    """c with its variables renamed x1, x2, ... in order: a renamed copy is not new."""
    names = {}
    order = sorted(c, key=lambda lit: (not lit[0], lit[1], show(Pred("", lit[2]))))
    for _, _, args in order:
        for a in args:
            for x in sorted(free(a)):
                names.setdefault(x, Var(f"x{len(names) + 1}"))
    return frozenset((s, p, tuple(once(a, names) for a in xs)) for s, p, xs in c)


def text(c):
    lits = sorted(("" if s else "~") + show(Pred(p, xs)) for s, p, xs in c)
    return " | ".join(lits) or "the empty clause"


def saturate(clauses, factoring):
    """Add resolvents (and factors) until the empty clause appears or nothing is new."""
    known = [normal(c) for c in clauses]
    for i, c in enumerate(known):
        print(f"  ({i + 1}) {text(c)}")
    grown = True
    while grown and frozenset() not in known:
        grown = False
        for i in range(len(known)):
            new = [(r, f"factor of ({i + 1})") for r, _ in factors(known[i])
                   if factoring]
            new += [(r, f"from ({j + 1}) and ({i + 1})")
                    for j in range(i + 1) for r, _ in resolvents(known[i], known[j])]
            for r, how in new:
                if normal(r) not in known:
                    known.append(normal(r))
                    print(f"  ({len(known)}) {text(normal(r))}   {how}")
                    grown = True
            if frozenset() in known:
                break
    end = "refuted" if frozenset() in known else "nothing new, no refutation"
    print(f"  {len(known)} clauses: {end}")


x, y = Var("x"), Var("y")
both = [frozenset({(True, "P", (x,)), (True, "P", (y,))}),      # P(x) | P(y)
        frozenset({(False, "P", (x,)), (False, "P", (y,))})]    # ~P(x) | ~P(y)
print("binary resolution alone:")
saturate(both, factoring=False)
print("with factoring:")
saturate(both, factoring=True)
