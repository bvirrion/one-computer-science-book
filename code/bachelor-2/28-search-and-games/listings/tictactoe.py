"""tictactoe.py: noughts and crosses solved by exhaustive search. A position is a
string of nine cells, 'x', 'o' or '.', and x moves first."""
from functools import cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6)]


def winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def to_move(b):
    return "x" if b.count("x") == b.count("o") else "o"


def moves(b):
    if winner(b) or "." not in b:
        return []
    p = to_move(b)
    return [b[:i] + p + b[i + 1:] for i in range(9) if b[i] == "."]


def score(b):
    """+1 if x has won, -1 if o has, 0 otherwise."""
    return {"x": 1, "o": -1, None: 0}[winner(b)]


@cache
def value(b):
    """The minimax value: x maximises, o minimises."""
    ms = moves(b)
    if not ms:
        return score(b)
    best = max if to_move(b) == "x" else min
    return best(value(m) for m in ms)


def count_tree(b):
    """Nodes and leaves of the full game tree below b."""
    ms = moves(b)
    if not ms:
        return 1, 1
    nodes, leaves = 1, 0
    for m in ms:
        n, f = count_tree(m)
        nodes, leaves = nodes + n, leaves + f
    return nodes, leaves


if __name__ == "__main__":
    empty = "." * 9
    print("value of the empty board:", value(empty))
    print("distinct positions reachable:", value.cache_info().currsize)
    nodes, leaves = count_tree(empty)
    print(f"game tree: {nodes} nodes, {leaves} finished games")
    print("x in the centre, then o in a corner:", value("o...x...."),
          "| o on an edge:", value(".o..x...."))
