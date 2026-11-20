"""minimax_demo.py: a game tree of depth 3, max to move at the root; its minimax
values, then the leaves alpha-beta evaluates and the ones it never looks at."""
import math

from alphabeta import alphabeta, minimax

TREE = [[[3, 5], [6, 9]], [[1, 2], [0, 7]], [[2, 1], [8, 4]]]
print("values of the min nodes:", [minimax(t, False, [0]) for t in TREE])
print("values of the max nodes below them:",
      [[minimax(u, True, [0]) for u in t] for t in TREE])
print("value of the root:", minimax(TREE, True, [0]))


def traced(node, maximise, alpha, beta, seen, label=""):
    """alphabeta, recording the labels of the leaves it evaluates."""
    if isinstance(node, int):
        seen.append(label)
        return node
    value = -math.inf if maximise else math.inf
    for i, c in enumerate(node):
        v = traced(c, not maximise, alpha, beta, seen, label + str(i))
        if maximise:
            value, alpha = max(value, v), max(alpha, v)
        else:
            value, beta = min(value, v), min(beta, v)
        if alpha >= beta:
            break
    return value


seen = []
print("alpha-beta value:", traced(TREE, True, -math.inf, math.inf, seen),
      "| leaves evaluated:", " ".join(seen), f"({len(seen)} of 12)")
assert traced(TREE, True, -math.inf, math.inf, []) == alphabeta(
    TREE, True, -math.inf, math.inf, [0])
