"""sort_game.py: swap two adjacent numbers that are out of order, until none is.

The variant is the number of inversions, pairs i < j with xs[i] > xs[j]: a swap
of an adjacent inverted pair removes exactly that inversion and changes no other."""


def inversions(xs):
    return sum(xs[i] > xs[j] for i in range(len(xs)) for j in range(i + 1, len(xs)))


def play(xs, choose=min):
    """Play until sorted; choose picks among the positions of inverted pairs."""
    xs, moves = list(xs), 0
    while True:
        out_of_order = [i for i in range(len(xs) - 1) if xs[i] > xs[i + 1]]
        if not out_of_order:
            return xs, moves
        i = choose(out_of_order)
        xs[i], xs[i + 1] = xs[i + 1], xs[i]
        moves += 1
