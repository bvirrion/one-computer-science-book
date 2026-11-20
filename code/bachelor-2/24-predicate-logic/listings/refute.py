"""refute.py: a resolution refutation of "p5 may not borrow", from the rules."""
from formulas import Not, Or, Pred, parse, show
from unify import resolvents

RULES = ["~Out(x, y) | Member(x)",  # whoever has a book out is a member
         "~Member(x) | MayBorrow(x)",  # members may borrow
         "Out(p5, b3)",  # a fact from the loans table
         "~MayBorrow(p5)"]  # the negation of the goal


def clause(text):
    """A disjunction of literals as a set of (sign, predicate, arguments)."""
    def literals(f):
        match f:
            case Or(a, b):
                return literals(a) | literals(b)
            case Not(p):
                return {(False, p.name, p.args)}
        return {(True, f.name, f.args)}
    return frozenset(literals(parse(text)))


def text(c):
    lits = [("" if sign else "~") + show(Pred(p, args)) for sign, p, args in sorted(c)]
    return " | ".join(lits) or "the empty clause"


known = [clause(r) for r in RULES]
for i, c in enumerate(known):
    print(f"({i + 1}) {text(c)}")
done = False
while not done:  # resolve every pair once more, until the empty clause appears
    for i, j in [(a, b) for a in range(len(known)) for b in range(a)]:
        for r, sigma in resolvents(known[i], known[j]):
            if r not in known:
                known.append(r)
                where = ", ".join(f"{x} := {show(t)}" for x, t in sorted(sigma.items()))
                line = f"({len(known)}) {text(r)}   from ({j + 1}) and ({i + 1})"
                print(f"{line} with {where}" if where else line)
                done = done or not r
        if done:
            break
