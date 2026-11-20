"""consistency.py -- four histories of reads and writes on registers x and y (all 0 at
first), each checked by brute force against four consistency models. An operation is
(client, kind, key, value, start, end), times on one real clock seen from outside."""

from itertools import permutations

H = {
    "H1": [("A", "w", "x", 1, 0, 2), ("B", "r", "x", 1, 3, 4)],
    "H2": [
        ("A", "w", "x", 1, 0, 1),
        ("B", "r", "x", 0, 2, 3),
        ("B", "r", "x", 1, 4, 5),
    ],
    "H3": [
        ("A", "w", "x", 1, 0, 1),
        ("B", "w", "y", 1, 0, 1),
        ("C", "r", "x", 1, 2, 3),
        ("C", "r", "y", 0, 4, 5),
        ("D", "r", "y", 1, 2, 3),
        ("D", "r", "x", 0, 4, 5),
        ("C", "r", "y", 1, 9, 9),
        ("D", "r", "x", 1, 9, 9),
    ],
    "H4": [
        ("A", "w", "x", 1, 0, 1),
        ("B", "r", "x", 1, 2, 3),
        ("B", "w", "y", 1, 4, 5),
        ("C", "r", "y", 1, 6, 7),
        ("C", "r", "x", 0, 8, 9),
        ("B", "r", "y", 1, 9, 9),
        ("C", "r", "x", 1, 9, 9),
    ],
}


def legal(order):
    """Every read returns the last value written before it in this order."""
    mem = {}
    for _, kind, key, value, *_ in order:
        if kind == "w":
            mem[key] = value
        elif mem.get(key, 0) != value:
            return False
    return True


def exists_order(ops, before):
    """Some legal order of ops in which a comes first whenever before(a, b)."""
    return any(
        legal(p) and all(not before(b, a) for i, a in enumerate(p) for b in p[i + 1 :])
        for p in permutations(ops)
    )


def program(a, b):
    return a[0] == b[0] and a[4] < b[4]


def linearisable(h):
    return exists_order(h, lambda a, b: a[5] < b[4])  # real time


def sequential(h):
    return exists_order(h, program)


def causal(h):
    """Program order plus write -> the reads of its value, closed; each client must see
    every write, and its own reads, in an order respecting it."""
    hb = {
        (a, b)
        for a in h
        for b in h
        if program(a, b) or (a[1] == "w" and b[1] == "r" and a[2:4] == b[2:4])
    }
    while True:
        more = {(a, d) for a, b in hb for c, d in hb if b == c} - hb
        if not more:
            break
        hb |= more
    return all(
        exists_order(
            [o for o in h if o[1] == "w" or o[0] == c], lambda a, b: (a, b) in hb
        )
        for c in {o[0] for o in h}
    )


def eventual(h):
    """Once the writes stop, every client's last read of a key returns one value."""
    last = {}
    for client, kind, key, value, *_ in sorted(h, key=lambda o: o[4]):
        if kind == "r":
            last[(client, key)] = value
    return all(
        len({v for (c, k), v in last.items() if k == key}) == 1
        for key in {k for _, k in last}
    )


if __name__ == "__main__":
    models = [linearisable, sequential, causal, eventual]
    print("     " + "".join(f"{m.__name__:>13}" for m in models))
    for name, h in H.items():
        print(f"{name:<5}" + "".join(f"{'yes' if m(h) else 'no':>13}" for m in models))
