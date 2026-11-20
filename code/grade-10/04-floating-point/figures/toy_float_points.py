"""Write toy_float_points.dat: every positive value of the 8-bit toy format."""
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).with_suffix(".dat")


def rows():
    for e in range(8):
        for f in range(16):
            value = (1 + Fraction(f, 16)) * Fraction(2) ** (e - 3)
            yield float(value), e


def main():
    lines = ["value exponent"] + [f"{v:.7f} {e}" for v, e in rows()]
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
