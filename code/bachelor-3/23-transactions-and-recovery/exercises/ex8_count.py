"""ex8_count.py -- two transactions, each reading then writing the items x1..xk in
order: how many of their interleavings are conflict serialisable? Counted by brute
force with schedules.py, then by the characterisation of the solution."""

import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from schedules import interleavings, parse, serial_order  # noqa: E402


def transactions(k):
    t1 = parse(" ".join(f"R1(x{i}) W1(x{i})" for i in range(k)))
    t2 = parse(" ".join(f"R2(x{i}) W2(x{i})" for i in range(k)))
    return t1, t2


def brute(k):
    return sum(serial_order(s) is not None for s in interleavings(*transactions(k)))


def by_rule(k):
    """Serialisable iff on every item one transaction's two operations both come
    before the other's, and it is the same transaction on every item."""
    count = 0
    for s in interleavings(*transactions(k)):
        first = set()
        for i in range(k):
            ops = [op[0] for op in s if op[2] == f"x{i}"]
            if ops[0] != ops[1]:  # the other transaction slipped in between
                break
            first.add(ops[0])
        else:
            count += len(first) == 1
    return count


if __name__ == "__main__":
    print(" k  interleavings  serialisable  by the rule  fraction")
    for k in range(1, 5):
        n, b = comb(4 * k, 2 * k), brute(k)
        print(f"{k:>2} {n:>14} {b:>13} {by_rule(k):>12} {b / n:>9.4f}")
