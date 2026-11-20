from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from gates import AND, OR, XOR  # noqa: E402


def half_adder(a, b):
    return XOR(a, b), AND(a, b)


def add_two_bits(a1, a0, b1, b0):
    """Add the two-bit numbers a1a0 and b1b0: three bits, carry first."""
    s0, c0 = half_adder(a0, b0)          # the units column
    t, c1 = half_adder(a1, b1)           # the twos column, without the carry
    s1, c2 = half_adder(t, c0)           # ... then with the carry
    return OR(c1, c2), s1, s0
