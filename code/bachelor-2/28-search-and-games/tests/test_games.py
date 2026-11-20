import math
import random
from functools import cache

from hypothesis import given, settings
from hypothesis import strategies as st

from alphabeta import alphabeta, best_first, minimax, random_tree
from games import attractor
from tictactoe import value


def brute_force_wins(owner, succ, target, p):
    """Positions from which p can force target within n moves, by the fixpoint of the
    one-step condition, computed naively."""
    win = set(target)
    while True:
        new = {u for u in owner if u not in win and (
            any(v in win for v in succ[u]) if owner[u] == p
            else all(v in win for v in succ[u]))}
        if not new:
            return win
        win |= new


@settings(max_examples=200, deadline=None)
@given(st.integers(0, 10**6))
def test_attractor_equals_brute_force(seed):
    rng = random.Random(seed)
    n = rng.randrange(1, 9)
    owner = {u: rng.randrange(2) for u in range(n)}
    succ = {u: sorted(rng.sample(range(n), rng.randrange(1, n + 1))) for u in range(n)}
    target = rng.sample(range(n), rng.randrange(0, n + 1))
    for p in (0, 1):
        layer, strategy = attractor(owner, succ, target, p)
        assert set(layer) == brute_force_wins(owner, succ, target, p)
        for u, v in strategy.items():  # the strategy moves one layer closer
            assert v in succ[u] and layer[v] < layer[u]


@settings(max_examples=100, deadline=None)
@given(st.integers(1, 4), st.integers(0, 5), st.integers(0, 10**6))
def test_alphabeta_equals_minimax(b, d, seed):
    tree = random_tree(b, d, random.Random(seed))
    for maximise in (True, False):
        v = minimax(tree, maximise, [0])
        assert alphabeta(tree, maximise, -math.inf, math.inf, [0]) == v
        count = [0]
        assert alphabeta(best_first(tree, maximise), maximise, -math.inf, math.inf,
                         count) == v
        assert count[0] <= b ** math.ceil(d / 2) + b ** (d // 2) - 1


def test_tictactoe_value():
    assert value("." * 9) == 0
    assert value(".o..x....") == 1


@cache
def matches_value(k):
    """+1 if the player to move with k matches wins, taking 1 to 3."""
    return 1 if any(matches_value(k - t) == -1 for t in (1, 2, 3) if t <= k) else -1


def test_matches_game():
    owner, succ = {}, {}
    for k in range(30):
        for p in "AB":
            owner[(k, p)] = p
            succ[(k, p)] = [(k - t, "B" if p == "A" else "A") for t in (1, 2, 3) if t <= k]
    win, _ = attractor(owner, succ, [(0, "B")], "A")
    assert all(((k, "A") in win) == (matches_value(k) == 1) for k in range(30))
    assert all((k, "A") in win for k in range(30) if k % 4)
