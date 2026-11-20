"""The checker accepts the book's proofs, refuses wrong steps, and is sound on the
propositional ones: every accepted conclusion follows from its hypotheses."""
import itertools

import pytest

import proofs
import proofs_more
from checker import ProofError, check
from checker import step as s
from exists_rules import EXISTS
from formulas import And, Bot, Imp, Not, Or, Pred, parse


def value(f, v):
    match f:
        case Pred(p, ()):
            return v[p]
        case Bot():
            return False
        case Not(a):
            return not value(a, v)
        case And(a, b):
            return value(a, v) and value(b, v)
        case Or(a, b):
            return value(a, v) or value(b, v)
        case Imp(a, b):
            return not value(a, v) or value(b, v)


def follows(hypotheses, goal, names="PQR"):
    for bits in itertools.product([False, True], repeat=len(names)):
        v = dict(zip(names, bits))
        if all(value(parse(h), v) for h in hypotheses) and not value(goal, v):
            return False
    return True


ACCEPTED = [proofs.MODUS_PONENS, proofs.SYLLOGISM, proofs.NO_COUNTEREXAMPLE,
            proofs.ALL, proofs_more.DE_MORGAN, proofs_more.SWAP,
            proofs_more.EXCLUDED_MIDDLE]


@pytest.mark.parametrize("case", ACCEPTED)
def test_accepted(case):
    hypotheses, proof = case
    assert check(proof, hypotheses, EXISTS) > 0


@pytest.mark.parametrize("case", [proofs.MODUS_PONENS, proofs.SYLLOGISM,
                                  proofs.NO_COUNTEREXAMPLE, proofs_more.DE_MORGAN,
                                  proofs_more.EXCLUDED_MIDDLE])
def test_propositional_conclusions_follow(case):
    hypotheses, proof = case
    assert follows(hypotheses, proof.goal)


@pytest.mark.parametrize("case, why", [
    (proofs.WRONG_ALL, "free in a hypothesis"),
    (proofs_more.CONVERSE, "free in a hypothesis"),
    ((["P"], s("hyp", "Q")), "not a hypothesis"),
    ((["P -> Q", "Q"], s("imp_e", "P", s("hyp", "P -> Q"), s("hyp", "Q"))), "premises"),
    ((["P"], s("imp_i", "Q -> P", s("hyp", "Q"))), "not A -> B"),
    ((["P & Q"], s("and_e1", "Q", s("hyp", "P & Q"))), "side"),
])
def test_refused(case, why):
    hypotheses, proof = case
    with pytest.raises(ProofError, match=why):
        check(proof, hypotheses, EXISTS)


def test_discharged_hypothesis_is_gone():
    """Once ->-introduction discharges P, a later use of P outside is refused."""
    proof = s("and_i", "(P -> P) & P",
              s("imp_i", "P -> P", s("hyp", "P")), s("hyp", "P"))
    with pytest.raises(ProofError, match="not a hypothesis"):
        check(proof, [])
