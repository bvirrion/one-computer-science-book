"""The harmonic sums 1 + 1/2 + ... + 1/n, exactly and in floating point."""
import math

from fraction import Fraction

exact, approx = Fraction(0), 0.0
for n in range(1, 1001):
    exact = exact + Fraction(1, n)
    approx += 1 / n
    if n <= 10 or n in (15, 20):
        lcm = math.lcm(*range(1, n + 1))
        print(f"H{n:<2} = {str(exact):>18}   lcm(1..{n}) = {lcm:>8}"
              f" = {lcm // exact.denominator()} x denominator")
    if n in (10, 100, 1000):
        print(f"  n = {n:4}: float sum {approx!r:<20} exact value {float(exact)!r:<20}"
              f" error {approx - float(exact):.1e}")
print("digits of the exact numerator for n = 1000:", len(str(exact.numerator())))
