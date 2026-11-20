"""exo_las_vegas.py: a number that is not a square modulo a prime p. Half the numbers
are not; Euler's criterion checks a candidate: a^((p-1)/2) = -1 mod p."""
import random

P = 2**61 - 1  # a prime


def is_nonresidue(a):
    return pow(a, (P - 1) // 2, P) == P - 1


def monte_carlo(rng, k):
    """At most k draws: the first that passes the check, else the last one, which is
    wrong. Wrong with probability 2^-k, and never more than k draws."""
    for _ in range(k):
        a = rng.randrange(1, P)
        if is_nonresidue(a):
            break
    return a


def las_vegas(rng):
    """Draw until the checker accepts: always right, 2 draws on average."""
    draws = 0
    while True:
        draws += 1
        a = rng.randrange(1, P)
        if is_nonresidue(a):
            return a, draws


rng = random.Random(12)
for k in [1, 3, 10]:
    wrong = sum(not is_nonresidue(monte_carlo(rng, k)) for _ in range(10_000))
    print(f"Monte Carlo, k = {k:2}: wrong in {wrong:4} of 10,000 runs;"
          f" 10,000 x 2^-k = {10_000 / 2**k:.1f}")
draws = [las_vegas(rng)[1] for _ in range(10_000)]
print(f"Las Vegas: always right; mean draws {sum(draws) / len(draws):.3f},"
      f" most {max(draws)}")
