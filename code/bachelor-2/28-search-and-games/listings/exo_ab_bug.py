"""exo_ab_bug.py: an alpha-beta that does not pass its bounds down to the children."""
import math
import random

from alphabeta import alphabeta, minimax, random_tree


def ab_short(node, maximise, count):
    if isinstance(node, int):
        count[0] += 1
        return node
    alpha, beta = -math.inf, math.inf  # fresh bounds at every node
    value = -math.inf if maximise else math.inf
    for c in node:
        v = ab_short(c, not maximise, count)
        if maximise:
            value, alpha = max(value, v), max(alpha, v)
        else:
            value, beta = min(value, v), min(beta, v)
        if alpha >= beta:
            break
    return value


rng = random.Random(2)
tree = random_tree(3, 6, rng)
for name, run in [("minimax", lambda c: minimax(tree, True, c)),
                  ("alpha-beta",
                   lambda c: alphabeta(tree, True, -math.inf, math.inf, c)),
                  ("fresh bounds", lambda c: ab_short(tree, True, c))]:
    count = [0]
    print(f"{name:12}: value {run(count)}, {count[0]} leaves")
