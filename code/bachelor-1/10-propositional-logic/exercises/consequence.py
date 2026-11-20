"""consequence.py: gamma |= phi, by trying every valuation."""

from evaluate import valuations, value
from formula import variables


def is_consequence(gamma, phi):
    """True when every valuation making all of gamma true makes phi true."""
    names = sorted(set(variables(phi)).union(*(variables(g) for g in gamma)))
    for v in valuations(names):
        if all(value(g, v) for g in gamma) and not value(phi, v):
            return False  # a counter-model
    return True
