"""Problem: a clock that adds a chopped tenth of a second at every tick."""
from fractions import Fraction

TENTH = Fraction(1, 10)


def chopped(x, bits):
    """x >= 0 chopped (rounded down) after `bits` binary places."""
    scale = 2**bits
    return Fraction(int(x * scale), scale)


def drift(hours, bits):
    """Seconds lost after `hours` of 0.1 s ticks, each worth chopped(0.1, bits)."""
    ticks = hours * 3600 * 10
    return ticks * (TENTH - chopped(TENTH, bits))


if __name__ == "__main__":
    for bits in (23, 24):
        error = TENTH - chopped(TENTH, bits)
        print(f"{bits} places: error per tick {float(error):.3e} s")
    for hours in (1, 8, 20, 48, 72, 100):
        print(f"{hours:3} h: drift {float(drift(hours, 23)):.4f} s (23 places)"
              f"  {float(drift(hours, 24)):.4f} s (24 places)")
