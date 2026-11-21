"""Unifiers unify and are most general; 2-SAT agrees with trying every assignment."""
import itertools

from hypothesis import given, settings
from hypothesis import strategies as st

from formulas import Fun, Var
from twosat import solve
from unify import factors, resolvents, unify, walk

terms = st.recursive(st.sampled_from([Var("x"), Var("y"), Var("z"), Fun("a"), Fun("b")]),
                     lambda t: st.builds(lambda u: Fun("f", (u,)), t)
                     | st.builds(lambda u, v: Fun("g", (u, v)), t, t),
                     max_leaves=5)


@settings(max_examples=500, deadline=None)
@given(terms, terms)
def test_unifier_unifies(s, t):
    sigma = unify(s, t)
    if sigma is not None:
        assert walk(s, sigma) == walk(t, sigma)


def once(t, tau):
    """t with every variable replaced at the same time, once."""
    match t:
        case Var(v):
            return tau.get(v, t)
        case Fun(f, args):
            return Fun(f, tuple(once(a, tau) for a in args))


@settings(max_examples=500, deadline=None)
@given(terms, terms, st.fixed_dictionaries({v: terms for v in "xyz"}))
def test_most_general(s, t, tau):
    """Any unifier tau is sigma followed by something: tau(sigma(v)) = tau(v)."""
    if once(s, tau) != once(t, tau):
        return
    sigma = unify(s, t)
    assert sigma is not None
    for v in "xyz":
        assert once(walk(Var(v), sigma), tau) == once(Var(v), tau)


def test_most_general_found():
    s, t = Fun("g", (Var("x"), Fun("a"))), Fun("g", (Var("y"), Var("z")))
    tau = {"x": Fun("b"), "y": Fun("b"), "z": Fun("a")}
    assert once(s, tau) == once(t, tau)
    sigma = unify(s, t)
    for v in "xyz":
        assert once(walk(Var(v), sigma), tau) == once(Var(v), tau)


def test_occurs_check():
    assert unify(Var("x"), Fun("f", (Var("x"),))) is None


def lit(sign, *args, p="P"):
    return (sign, p, tuple(args))


def test_factor():
    x, y = Var("x"), Var("y")
    c = frozenset({lit(True, x), lit(True, Fun("f", (y,))), lit(True, x, p="Q")})
    found = [f for f, _ in factors(c)]
    assert found == [frozenset({lit(True, Fun("f", (y,))), lit(True, Fun("f", (y,)), p="Q")})]
    assert list(factors(frozenset({lit(True, x), lit(False, y)}))) == []


def shape(c):
    """A clause on the unary P, up to renaming: its signs and its number of variables."""
    return tuple(sorted(s for s, _, _ in c)), len({a for _, _, args in c for a in args})


def test_binary_resolution_alone_is_incomplete():
    """P(x) | P(y) and ~P(x) | ~P(y) have no model; their binary resolvents, up to
    renaming, are closed among three clauses of two literals: no empty clause."""
    x, y = Var("x"), Var("y")
    pos, neg = frozenset({lit(True, x), lit(True, y)}), frozenset({lit(False, x), lit(False, y)})
    mixed = frozenset({lit(True, x), lit(False, y)})
    closed = {shape(pos), shape(neg), shape(mixed)}
    for a in (pos, neg, mixed):
        for b in (pos, neg, mixed):
            for r, _ in resolvents(a, b):
                assert len(r) == 2 and shape(r) in closed


def test_factoring_refutes():
    x, y = Var("x"), Var("y")
    pos, neg = frozenset({lit(True, x), lit(True, y)}), frozenset({lit(False, x), lit(False, y)})
    (p1, _), = factors(pos)
    (n1, _), = factors(neg)
    assert frozenset() in [r for r, _ in resolvents(p1, n1)]


literals = st.integers(1, 5).flatmap(lambda k: st.sampled_from([k, -k]))


@settings(max_examples=500, deadline=None)
@given(st.lists(st.tuples(literals, literals), max_size=14))
def test_twosat_against_brute_force(clauses):
    def true(lit, a):
        return a[abs(lit) - 1] == (lit > 0)

    sat = any(all(true(x, a) or true(y, a) for x, y in clauses)
              for a in itertools.product([False, True], repeat=5))
    found, bad = solve(5, clauses)
    assert (found is not None) == sat
    if found:
        a = [found[k] for k in range(1, 6)]
        assert all(true(x, a) or true(y, a) for x, y in clauses)
