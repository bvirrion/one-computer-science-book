"""alphabeta.py: minimax and alpha-beta on uniform random trees, counting the leaves
evaluated, with the children in random order and in the best order."""
import math
import random


def minimax(node, maximise, count):
    if isinstance(node, int):
        count[0] += 1
        return node
    values = [minimax(c, not maximise, count) for c in node]
    return max(values) if maximise else min(values)


def alphabeta(node, maximise, alpha, beta, count):
    """The minimax value if it lies strictly between alpha and beta; otherwise a bound
    on the same side as the true value."""
    if isinstance(node, int):
        count[0] += 1
        return node
    if maximise:
        value = -math.inf
        for c in node:
            value = max(value, alphabeta(c, False, alpha, beta, count))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # min above will never let play come here
        return value
    value = math.inf
    for c in node:
        value = min(value, alphabeta(c, True, alpha, beta, count))
        beta = min(beta, value)
        if alpha >= beta:
            break  # max above already has better
    return value


def random_tree(b, d, rng):
    if d == 0:
        return rng.randrange(1000)
    return [random_tree(b, d - 1, rng) for _ in range(b)]


def best_first(node, maximise):
    """The same tree with the children sorted best first for the player to move."""
    if isinstance(node, int):
        return node
    kids = [best_first(c, not maximise) for c in node]
    kids.sort(key=lambda c: minimax(c, not maximise, [0]), reverse=maximise)
    return kids


if __name__ == "__main__":
    rng = random.Random(1)
    print(" b  d  leaves   alpha-beta, random order  best order"
          "  b^ceil(d/2)+b^floor(d/2)-1")
    for b, d in [(3, 6), (4, 6), (4, 8), (8, 5)]:
        tree = random_tree(b, d, rng)
        c0, c1, c2 = [0], [0], [0]
        v0 = minimax(tree, True, c0)
        v1 = alphabeta(tree, True, -math.inf, math.inf, c1)
        v2 = alphabeta(best_first(tree, True), True, -math.inf, math.inf, c2)
        assert v0 == v1 == v2
        bound = b ** math.ceil(d / 2) + b ** (d // 2) - 1
        print(f"{b:2} {d:2} {c0[0]:7} {c1[0]:25} {c2[0]:11} {bound:28}")
