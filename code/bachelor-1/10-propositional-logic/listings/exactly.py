"""exactly.py: "exactly one of these literals is true", as clauses."""

from itertools import combinations

from quine import neg


def exactly_one(lits):
    """One clause says "at least one"; one clause per pair says "not both"."""
    at_least = [frozenset(lits)]
    at_most = [frozenset([neg(a), neg(b)]) for a, b in combinations(lits, 2)]
    return at_least + at_most
