"""The substitution lemma, parsing and printing, on random formulas."""
from hypothesis import given, settings
from hypothesis import strategies as st

from formulas import (And, Bot, Exists, Forall, Fun, Imp, Not, Or, Pred, Var, free,
                      parse, show, subst)
from structures import Structure

VARS = ["x", "y", "z"]
terms = st.recursive(st.sampled_from([Var(v) for v in VARS] + [Fun("c")]),
                     lambda t: st.builds(lambda a: Fun("s", (a,)), t)
                     | st.builds(lambda a, b: Fun("g", (a, b)), t, t),
                     max_leaves=4)
atoms = st.one_of(st.builds(lambda a: Pred("P", (a,)), terms),
                  st.builds(lambda a, b: Pred("R", (a, b)), terms, terms),
                  st.builds(lambda a, b: Pred("=", (a, b)), terms, terms),
                  st.just(Bot()))
formulas = st.recursive(
    atoms,
    lambda f: st.builds(Not, f) | st.builds(And, f, f) | st.builds(Or, f, f)
    | st.builds(Imp, f, f) | st.builds(Forall, st.sampled_from(VARS), f)
    | st.builds(Exists, st.sampled_from(VARS), f),
    max_leaves=6)

A = Structure(range(3), {"P": {(0,), (2,)}, "R": {(0, 1), (1, 2), (2, 2), (1, 0)}},
              {"s": lambda a: (a + 1) % 3, "g": lambda a, b: (a * b + 1) % 3,
               "c": lambda: 2})
envs = st.fixed_dictionaries({v: st.integers(0, 2) for v in VARS})


@settings(max_examples=400, deadline=None)
@given(formulas, st.sampled_from(VARS), terms, envs)
def test_substitution_lemma(phi, x, t, env):
    """A, env |= phi[t/x]  iff  A, env[x := value of t] |= phi."""
    assert A.holds(subst(phi, x, t), env) == A.holds(phi, {**env, x: A.value(t, env)})


@settings(max_examples=400, deadline=None)
@given(formulas, st.sampled_from(VARS), terms)
def test_substitution_free_variables(phi, x, t):
    expected = (free(phi) - {x}) | (free(t) if x in free(phi) else set())
    assert free(subst(phi, x, t)) == expected


@settings(max_examples=400, deadline=None)
@given(formulas)
def test_show_then_parse(phi):
    assert parse(show(phi)) == phi


def test_capture_is_avoided():
    phi = parse("exists y. y = s(x)")
    assert show(subst(phi, "x", Var("y"))) == "exists y1. y1 = s(y)"
    assert subst(phi, "y", Var("z")) == phi  # y is bound: nothing to replace


def test_town_rules():
    from structures import town
    T = town()
    assert T.holds(parse("forall x. (exists y. Out(x, y)) -> Member(x)"))
    assert not T.holds(parse("forall x. Member(x) -> exists y. Friend(x, y)"))
