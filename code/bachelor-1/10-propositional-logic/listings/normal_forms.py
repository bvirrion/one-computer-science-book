"""normal_forms.py: negation normal form, then CNF and DNF by distribution."""

from formula import Bin, Not, Var, iff


def nnf(f, positive=True):
    """An equivalent formula of & and | over literals (of ~f if not positive)."""
    match f:
        case Var():
            return f if positive else Not(f)
        case Not(sub):
            return nnf(sub, not positive)
        case Bin("->", a, b):
            return nnf(~a | b, positive)
        case Bin("<->", a, b):
            return nnf((a >> b) & (b >> a), positive)
        case Bin(op, a, b):  # & or |; De Morgan swaps them under a negation
            if not positive:
                op = "|" if op == "&" else "&"
            return Bin(op, nnf(a, positive), nnf(b, positive))


def literal(g):
    return g.name if isinstance(g, Var) else "~" + g.sub.name


def distribute(g, outer, inner):
    """g in NNF, as a list of sets of literals: an `outer` of `inner`s."""
    match g:
        case Bin(op, a, b) if op == outer:
            return distribute(a, outer, inner) + distribute(b, outer, inner)
        case Bin(op, a, b) if op == inner:
            return [x | y for x in distribute(a, outer, inner)
                    for y in distribute(b, outer, inner)]
        case _:
            return [frozenset([literal(g)])]


def cnf(f):
    return distribute(nnf(f), "&", "|")


def dnf(f):
    return distribute(nnf(f), "|", "&")


def simplify(sets):
    """Drop the sets holding a literal and its negation, and repeated sets."""
    seen, out = set(), []
    for s in sets:
        if not any("~" + x in s for x in s) and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def key(lit):
    return lit.lstrip("~"), lit.startswith("~")


def show_sets(sets, outer, inner):
    return f" {outer} ".join("(" + f" {inner} ".join(sorted(s, key=key)) + ")"
                             for s in sets)


if __name__ == "__main__":
    p, q, r = Var("p"), Var("q"), Var("r")
    for f in [~((p >> q) | r), iff(p, q) | r]:
        print("formula:", f)
        print("  NNF:", nnf(f))
        print("  CNF:", show_sets(cnf(f), "&", "|"))
        print("  CNF simplified:", show_sets(simplify(cnf(f)), "&", "|"))
        print("  DNF:", show_sets(dnf(f), "|", "&"))
        print("  DNF simplified:", show_sets(simplify(dnf(f)), "|", "&"))
