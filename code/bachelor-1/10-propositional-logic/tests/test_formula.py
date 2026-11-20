"""Formulas, evaluation and normal forms, checked on random formulas."""

import sys
from itertools import product
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from blowup import pairs  # noqa: E402
from consequence import is_consequence  # noqa: E402
from evaluate import is_tautology, models, valuations, value  # noqa: E402
from exactly import exactly_one  # noqa: E402
from formula import Bin, Not, Var, height, iff, size, subformulas, variables  # noqa: E402
from normal_forms import cnf, dnf, nnf, simplify  # noqa: E402
from quine import satisfies  # noqa: E402
from truth_table import complete_dnf  # noqa: E402
from tseitin import tseitin  # noqa: E402

NAMES = ["p", "q", "r", "s"]
formulas = st.recursive(
    st.sampled_from(NAMES).map(Var),
    lambda sub: st.one_of(sub.map(Not),
                          st.tuples(st.sampled_from(["&", "|", "->", "<->"]), sub, sub)
                          .map(lambda t: Bin(*t))),
    max_leaves=10)


def all_valuations():
    return list(valuations(NAMES))


def holds(sets, v, outer_and):
    def lit(x):
        return not v[x[1:]] if x.startswith("~") else v[x]
    if outer_and:
        return all(any(lit(x) for x in c) for c in sets)
    return any(all(lit(x) for x in c) for c in sets)


@given(formulas)
def test_nnf_cnf_dnf_equivalent(f):
    g, c, d = nnf(f), cnf(f), dnf(f)
    for v in all_valuations():
        assert value(g, v) == value(f, v)
        assert holds(c, v, True) == value(f, v) == holds(simplify(c), v, True)
        assert holds(d, v, False) == value(f, v) == holds(simplify(d), v, False)
    assert all(isinstance(h, Var) or isinstance(h, Bin) and h.op in "&|"
               or isinstance(h, Not) and isinstance(h.sub, Var) for h in subformulas(g))


@given(formulas)
def test_size_height(f):
    assert height(f) < size(f) <= 2 ** (height(f) + 1) - 1
    assert len(subformulas(f)) <= size(f)


@given(formulas)
@settings(max_examples=60)
def test_tseitin_equisatisfiable(f):
    clauses = tseitin(f)
    assert len(clauses) <= 2 * size(f) - 1
    names = sorted({x.lstrip("~") for c in clauses for x in c})
    sat = any(satisfies({x if b else "~" + x for x, b in zip(names, bits)}, clauses)
              for bits in product([False, True], repeat=len(names)))
    assert sat == bool(models(f))


@given(formulas)
def test_complete_dnf_has_one_term_per_model(f):
    text = complete_dnf(f)
    assert text.count("(") == len(models(f))


def test_blowup_counts():
    for n in range(1, 9):
        assert len(cnf(pairs(n))) == len(simplify(cnf(pairs(n)))) == 2 ** n
        assert size(pairs(n)) == 4 * n - 1


def test_exactly_one():
    for n in range(1, 7):
        lits = [f"x{i}" for i in range(n)]
        clauses = exactly_one(lits)
        assert len(clauses) == n * (n - 1) // 2 + 1
        good = 0
        for bits in product([False, True], repeat=n):
            model = {x if b else "~" + x for x, b in zip(lits, bits)}
            good += satisfies(model, clauses)
            assert satisfies(model, clauses) == (sum(bits) == 1)
        assert good == n


@given(st.lists(formulas, max_size=3), formulas)
def test_consequence(gamma, phi):
    conj = gamma[0] if gamma else phi | ~phi
    for g in gamma[1:]:
        conj = conj & g
    assert is_consequence(gamma, phi) == is_tautology(conj >> phi if gamma else phi)


def test_consequence_examples():
    p, q = Var("p"), Var("q")
    assert is_consequence([p, p >> q], q)
    assert not is_consequence([q, p >> q], p)
    assert is_consequence([p, ~p], q)
    assert variables(iff(p, q)) == ["p", "q"]
