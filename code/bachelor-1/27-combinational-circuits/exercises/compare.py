"""compare.py: a < b for 4-bit unsigned numbers: at the most significant bit where they
differ, a has 0 and b has 1."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from circuit import Circuit  # noqa: E402


def less_than():
    c = Circuit(*[f"a{i}" for i in range(4)], *[f"b{i}" for i in range(4)])
    eq = [c.gate("NOT", c.gate("XOR", f"a{i}", f"b{i}")) for i in range(4)]
    lt = [c.gate("AND", c.gate("NOT", f"a{i}"), f"b{i}") for i in range(4)]
    terms = [c.gate("AND", lt[i], *eq[i + 1:]) if i < 3 else lt[3] for i in range(4)]
    c.outputs["lt"] = c.gate("OR", *terms)
    return c
