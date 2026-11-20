from fractions import Fraction


def toy_value(e, f):
    """Value of the pattern with exponent field e (0..7), fraction field f (0..15)."""
    return (1 + Fraction(f, 16)) * Fraction(2) ** (e - 3)


values = sorted(toy_value(e, f) for e in range(8) for f in range(16))
print(len(values), "positive values, from", values[0], "to", values[-1])
for e in range(8):
    low = toy_value(e, 0)
    gap = toy_value(e, 1) - low
    high = toy_value(e, 15)
    print(f"exponent field {e}: from {str(low):>4} to {str(high):>6}, gap {gap}")
