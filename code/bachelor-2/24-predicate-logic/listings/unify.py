"""unify.py: Robinson's unification with the occurs check, and resolution on clauses."""
from formulas import Fun, Var, free


def walk(t, sigma):
    """t with the bindings of sigma applied, all the way down."""
    match t:
        case Var(x) if x in sigma:
            return walk(sigma[x], sigma)
        case Fun(f, args):
            return Fun(f, tuple(walk(a, sigma) for a in args))
    return t


def unify(s, t, sigma=None):
    """A most general unifier of s and t extending sigma, as a dict, or None."""
    sigma = dict(sigma or {})
    todo = [(s, t)]
    while todo:
        a, b = (walk(u, sigma) for u in todo.pop())
        match a, b:
            case _ if a == b:
                continue
            case Var(x), _:
                if x in free(b):
                    return None  # the occurs check: x = f(x) has no finite solution
                sigma[x] = b
            case _, Var(_):
                todo.append((b, a))
            case Fun(f, xs), Fun(g, ys) if f == g and len(xs) == len(ys):
                todo.extend(zip(xs, ys))
            case _:
                return None  # two different function symbols: a clash
    return sigma


def rename(literal, suffix):
    """A copy of (sign, name, args) with its variables renamed apart."""
    sign, name, args = literal
    sigma = {x: Var(x + suffix) for a in args for x in free(a)}
    return sign, name, tuple(walk(a, sigma) for a in args)


def resolvents(c1, c2):
    """Every resolvent of two clauses, sets of literals (sign, predicate, arguments)."""
    c2 = frozenset(rename(lit, "'") for lit in c2)  # no variable shared with c1
    for sign, p, args in c1:
        for sign2, p2, args2 in c2:
            if p != p2 or sign == sign2:
                continue
            sigma = unify(Fun("", args), Fun("", args2))
            if sigma is not None:  # L and the negation of L' made equal by sigma
                rest = (c1 - {(sign, p, args)}) | (c2 - {(sign2, p2, args2)})
                yield frozenset((sg, q, tuple(walk(a, sigma) for a in xs))
                                for sg, q, xs in rest), sigma
