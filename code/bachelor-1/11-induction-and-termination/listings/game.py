"""game.py: replace some k > 0 by two copies of k - 1, until only zeros remain."""

from functools import cache


def moves(state):
    """Every state one move away; a state is a tuple of natural numbers."""
    return [state[:i] + (k - 1, k - 1) + state[i + 1:]
            for i, k in enumerate(state) if k > 0]


@cache
def lengths(state):
    """The set of lengths of all plays from state."""
    nxt = moves(state)
    if not nxt:
        return frozenset([0])
    return frozenset(1 + n for s in nxt for n in lengths(s))


@cache
def plays(state):
    """The number of different plays from state."""
    nxt = moves(state)
    return 1 if not nxt else sum(plays(s) for s in nxt)


def potential(state):
    return sum(2 ** a - 1 for a in state)


if __name__ == "__main__":
    print(f"{'start':12} {'potential':>9} {'play lengths':>13} {'plays':>12}")
    for start in [(1,), (2,), (3,), (4,), (1, 2), (2, 2, 1), (3, 1, 0), (3, 3)]:
        found = sorted(lengths(start))
        print(f"{str(start):12} {potential(start):9d} {str(found):>13}"
              f" {plays(start):12d}")
