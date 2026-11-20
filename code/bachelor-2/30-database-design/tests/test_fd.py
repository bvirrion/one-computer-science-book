import random
from itertools import combinations

from hypothesis import given, settings
from hypothesis import strategies as st

from fd import (bcnf, bcnf_violation, closure, is_3nf, keys, lossless, minimal_cover,
                preserves, synthesis_3nf)

U = "abcd"


def all_subsets(attrs):
    return [frozenset(c) for n in range(len(attrs) + 1) for c in combinations(attrs, n)]


def armstrong(deps, attrs=U):
    """Every X -> Y derivable by reflexivity, augmentation and transitivity."""
    subs = all_subsets(attrs)
    known = {(x, y) for x in subs for y in subs if y <= x} | set(deps)
    while True:
        new = {(x | z, y | z) for x, y in known for z in subs}
        by_left = {}
        for x, y in known:
            by_left.setdefault(x, set()).add(y)
        new |= {(x, z) for x, y in known for z in by_left.get(y, ())}
        if new <= known:
            return known
        known |= new


def random_deps(rng, attrs=U, n=None):
    subs = [s for s in all_subsets(attrs) if s]
    return [(rng.choice(subs), frozenset([rng.choice(attrs)]))
            for _ in range(rng.randrange(0, 5) if n is None else n)]


@settings(max_examples=40, deadline=None)
@given(st.integers(0, 10**6))
def test_closure_equals_armstrong_saturation(seed):
    rng = random.Random(seed)
    deps = random_deps(rng)
    derived = armstrong(deps)
    for x in all_subsets(U):
        assert {a for a in U if (x, frozenset(a)) in derived} == set(closure(x, deps))


def satisfying_instance(rng, attrs, deps, rows=8, domain=3):
    """Random rows, then repaired until every dependency holds."""
    r = [{a: rng.randrange(domain) for a in attrs} for _ in range(rows)]
    for _ in range(50):
        changed = False
        for left, right in deps:
            first = {}
            for row in r:
                key = tuple(row[a] for a in sorted(left))
                ref = first.setdefault(key, row)
                for a in right:
                    if row[a] != ref[a]:
                        row[a], changed = ref[a], True
        if not changed:
            return {tuple(row[a] for a in attrs) for row in r}
    return None


def join_of_projections(instance, attrs, parts):
    rows = [dict(zip(attrs, t)) for t in instance]
    result = [{}]
    for p in parts:
        proj = {tuple(sorted((a, row[a]) for a in p)) for row in rows}
        result = [dict(r, **dict(t)) for r in result for t in proj
                  if all(r.get(a, v) == v for a, v in t)]
    return {tuple(r[a] for a in attrs) for r in result}


@settings(max_examples=150, deadline=None)
@given(st.integers(0, 10**6))
def test_lossless_by_chase_on_random_instances(seed):
    rng = random.Random(seed)
    attrs = "abcde"
    deps = random_deps(rng, attrs, rng.randrange(1, 5))
    subs = [s for s in all_subsets(attrs) if s]
    parts = [rng.choice(subs) for _ in range(rng.randrange(2, 4))]
    parts.append(frozenset(attrs) - frozenset().union(*parts) or parts[0])
    inst = satisfying_instance(rng, attrs, deps)
    if inst is None:
        return
    joined = join_of_projections(inst, attrs, parts)
    assert inst <= joined  # a join of projections never loses a row
    if lossless(attrs, parts, deps):
        assert joined == inst


@settings(max_examples=150, deadline=None)
@given(st.integers(0, 10**6))
def test_bcnf_and_synthesis(seed):
    rng = random.Random(seed)
    attrs = "abcde"
    deps = random_deps(rng, attrs, rng.randrange(1, 6))
    r = frozenset(attrs)
    parts = bcnf(r, deps)
    assert lossless(r, parts, deps)
    assert all(bcnf_violation(p, deps) is None for p in parts)
    syn = synthesis_3nf(r, deps)
    assert lossless(r, syn, deps) and preserves(syn, deps)
    assert all(is_3nf(p, deps) for p in syn)
    cover = minimal_cover(deps)
    for x in all_subsets(attrs):
        assert closure(x, cover) == closure(x, deps)
    for k in keys(r, deps):
        assert closure(k, deps) == r
        assert all(closure(k - {a}, deps) != r for a in k)


def test_superkeys_of_a_single_key():
    """With one key of size k among n attributes, there are 2^(n-k) superkeys."""
    attrs = "abcdef"
    deps = [(frozenset("ab"), frozenset("cdef"))]
    supers = [s for s in all_subsets(attrs) if closure(s, deps) == frozenset(attrs)]
    assert len(supers) == 2 ** (6 - 2)
