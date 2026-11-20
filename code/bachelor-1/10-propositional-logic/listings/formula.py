"""formula.py: propositional formulas as trees."""

from dataclasses import dataclass


class Formula:
    """Python's operators build formulas: ~p, p & q, p | q, p >> q (implies)."""

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return Bin("&", self, other)

    def __or__(self, other):
        return Bin("|", self, other)

    def __rshift__(self, other):
        return Bin("->", self, other)

    def __str__(self):
        return show(self)


@dataclass(frozen=True)
class Var(Formula):
    name: str


@dataclass(frozen=True)
class Not(Formula):
    sub: Formula


@dataclass(frozen=True)
class Bin(Formula):
    op: str  # "&", "|", "->" or "<->"
    left: Formula
    right: Formula


def iff(a, b):
    return Bin("<->", a, b)


def size(f):
    match f:
        case Var():
            return 1
        case Not(sub):
            return 1 + size(sub)
        case Bin(_, left, right):
            return 1 + size(left) + size(right)


def height(f):
    match f:
        case Var():
            return 0
        case Not(sub):
            return 1 + height(sub)
        case Bin(_, left, right):
            return 1 + max(height(left), height(right))


def subformulas(f):
    match f:
        case Var():
            return {f}
        case Not(sub):
            return {f} | subformulas(sub)
        case Bin(_, left, right):
            return {f} | subformulas(left) | subformulas(right)


def variables(f):
    return sorted(g.name for g in subformulas(f) if isinstance(g, Var))


PREC = {"<->": 1, "->": 2, "|": 3, "&": 4}  # Not binds tighter than all of them


def show(f, outer=0):
    """Write f with only the parentheses needed; & and | group to the left,
    -> to the right, and <-> is always parenthesised inside itself."""
    match f:
        case Var(name):
            return name
        case Not(sub):
            return "~" + show(sub, 5)
        case Bin(op, left, right):
            p = PREC[op]
            right_assoc = op == "->"
            text = (show(left, p + (right_assoc or op == "<->"))
                    + f" {op} "
                    + show(right, p + (not right_assoc)))
            return f"({text})" if p < outer else text


def tree(f, depth=0):
    """The tree of f, one node per line, children indented under their parent."""
    pad = "    " * depth
    match f:
        case Var(name):
            return [pad + name]
        case Not(sub):
            return [pad + "~"] + tree(sub, depth + 1)
        case Bin(op, left, right):
            return [pad + op] + tree(left, depth + 1) + tree(right, depth + 1)


if __name__ == "__main__":
    p, q, r = Var("p"), Var("q"), Var("r")
    f = (p >> q) & ~(q | r)
    print("formula:", f)
    print("\n".join(tree(f)))
    print("size", size(f), "height", height(f), "variables", variables(f))
    subs = sorted(map(str, subformulas(f)), key=lambda s: (len(s), s))
    print(len(subs), "subformulas:", subs)
    for g in [p & (q & r), (p & q) & r, p >> (q >> r), (p >> q) >> r,
              ~(p | q) | ~p, iff(p, iff(q, r))]:
        print(g)
