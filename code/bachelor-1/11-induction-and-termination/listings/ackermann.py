"""ackermann.py: Ackermann's function, its values and its number of calls."""

import sys

sys.setrecursionlimit(100_000)
calls = 0


def ack(m, n):
    global calls
    calls += 1
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))


if __name__ == "__main__":
    print("m\\n" + "".join(f"{n:>14}" for n in range(5)))
    for m in range(4):
        row = []
        for n in range(5):
            calls = 0
            row.append(f"{ack(m, n)} ({calls})")
        print(f"{m:3}" + "".join(f"{cell:>14}" for cell in row))
