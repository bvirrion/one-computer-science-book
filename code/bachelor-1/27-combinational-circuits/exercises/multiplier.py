"""multiplier.py: a 4-bit array multiplier: the partial products a_i b_j by AND gates,
added row by row with ripple-carry adders."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from adders import full_adder  # noqa: E402
from circuit import Circuit  # noqa: E402


def multiplier(n=4):
    c = Circuit(*[f"a{i}" for i in range(n)], *[f"b{i}" for i in range(n)])
    zero = c.gate("AND", "a0", c.gate("NOT", "a0"))
    acc = [c.gate("AND", f"a{i}", "b0") for i in range(n)] + [zero] * n
    for j in range(1, n):  # add (a AND b_j) shifted j places
        row = [c.gate("AND", f"a{i}", f"b{j}") for i in range(n)]
        carry = zero
        for i in range(n):
            acc[i + j], carry = full_adder(c, acc[i + j], row[i], carry)
        acc[n + j] = carry
    for k, w in enumerate(acc):
        c.outputs[f"p{k}"] = w
    return c
