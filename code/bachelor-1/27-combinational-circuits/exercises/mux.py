"""mux.py: 2-to-1 and 4-to-1 multiplexers in the simulator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from circuit import Circuit  # noqa: E402


def mux2(c, s, x0, x1):
    return c.gate("OR", c.gate("AND", c.gate("NOT", s), x0), c.gate("AND", s, x1))


def mux4():
    """Output x[2 s1 + s0]: two levels of 2-to-1 multiplexers."""
    c = Circuit("s1", "s0", "x0", "x1", "x2", "x3")
    low, high = mux2(c, "s0", "x0", "x1"), mux2(c, "s0", "x2", "x3")
    c.outputs["out"] = mux2(c, "s1", low, high)
    return c
