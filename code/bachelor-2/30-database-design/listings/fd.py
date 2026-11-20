"""fd.py: functional dependencies. An attribute is a string, a set of attributes a
frozenset, a dependency X -> Y a pair of frozensets."""
from itertools import combinations


def fds(text):
    """Parse "a b -> c; c -> d" into a list of dependencies."""
    out = []
    for part in text.split(";"):
        left, right = part.split("->")
        out.append((frozenset(left.split()), frozenset(right.split())))
    return out


def closure(xs, deps):
    """X+: every attribute that X determines under deps."""
    result, changed = set(xs), True
    while changed:
        changed = False
        for left, right in deps:
            if left <= result and not right <= result:
                result |= right  # X determines left, hence right
                changed = True
    return frozenset(result)


def implies(deps, left, right):
    return right <= closure(left, deps)


def keys(attrs, deps):
    """The candidate keys: the minimal sets whose closure is every attribute."""
    attrs = frozenset(attrs)
    found = []
    for size in range(len(attrs) + 1):
        for xs in combinations(sorted(attrs), size):
            xs = frozenset(xs)
            if not any(k <= xs for k in found) and closure(xs, deps) >= attrs:
                found.append(xs)
    return found


def minimal_cover(deps):
    """An equivalent set with one attribute on each right side, no extraneous
    attribute on a left side, and no redundant dependency."""
    out = [(left, frozenset([a])) for left, right in deps for a in sorted(right)]
    for i, (left, right) in enumerate(out):
        for a in sorted(left):
            if len(left) > 1 and right <= closure(left - {a}, out):
                left = left - {a}  # a is extraneous on the left
        out[i] = (left, right)
    out = list(dict.fromkeys(out))
    for d in list(out):
        rest = [e for e in out if e != d]
        if implies(rest, *d):
            out = rest
    return out


def subsets(attrs):
    attrs = sorted(attrs)
    for size in range(1, len(attrs) + 1):
        for xs in combinations(attrs, size):
            yield frozenset(xs)


def bcnf_violation(r, deps):
    """A dependency X -> Y that holds in r with X not a superkey of r, or None."""
    r = frozenset(r)
    for xs in subsets(r):
        c = closure(xs, deps) & r
        if c != xs and c != r:
            return xs, c - xs
    return None


def bcnf(r, deps):
    """Split r on a violating X -> Y into XY and r - Y, until no part has one."""
    v = bcnf_violation(r, deps)
    if v is None:
        return [frozenset(r)]
    xs, ys = v
    return bcnf(xs | ys, deps) + bcnf(frozenset(r) - ys, deps)


def is_3nf(r, deps):
    """Every X -> A holding in r, A not in X, has X a superkey or A in some key."""
    r = frozenset(r)
    prime = frozenset().union(*keys(r, deps))
    for xs in subsets(r):
        c = closure(xs, deps) & r
        if c != r and not (c - xs) <= prime:
            return False
    return True


def synthesis_3nf(r, deps):
    """One table per left side of a minimal cover, plus a key if none holds one."""
    groups = {}
    for left, right in minimal_cover(deps):
        groups[left] = groups.get(left, left) | right
    parts = list(dict.fromkeys(groups.values()))
    parts = [p for p in parts if not any(p < q for q in parts)]
    if not any(closure(p, deps) >= frozenset(r) for p in parts):
        parts.append(keys(r, deps)[0])
    return parts


def lossless(r, parts, deps):
    """The chase: a row per part, equal symbols forced by the dependencies; the join
    of the projections is lossless iff some row ends with every attribute 'a'."""
    rows = [{a: "a" if a in p else (i, a) for a in r} for i, p in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for left, right in deps:
            for s in rows:
                for t in rows:
                    if all(s[a] == t[a] for a in left):
                        for a in right:
                            if s[a] != t[a]:
                                new = "a" if "a" in (s[a], t[a]) else min(s[a], t[a])
                                old = {s[a], t[a]} - {new}
                                for u in rows:  # rename the symbol everywhere
                                    if u[a] in old:
                                        u[a] = new
                                changed = True
    return any(all(v == "a" for v in row.values()) for row in rows)


def preserves(parts, deps):
    """Every dependency follows from the dependencies that hold inside the parts."""
    for left, right in deps:
        z, changed = set(left), True
        while changed:
            changed = False
            for p in parts:
                more = closure(frozenset(z) & p, deps) & p
                if not more <= z:
                    z |= more
                    changed = True
        if not right <= z:
            return False
    return True
