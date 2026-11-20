"""The listener's attack: try a = 1, 2, 3, ... until g**a mod p equals A."""
import random


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


def prime_factors(n):
    factors, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    return factors | ({n} if n > 1 else set())


def generator(p):
    """The smallest g whose powers give every number from 1 to p - 1."""
    qs = prime_factors(p - 1)
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in qs))


def brute_force(p, g, A):
    """Return Alice's secret and the number of multiplications it took."""
    value, a = g, 1
    while value != A:
        value, a = value * g % p, a + 1
    return a, a - 1


rng = random.Random(7)
for bits in range(10, 25, 2):
    p = next(n for n in range(2**bits - 1, 0, -1) if is_prime(n))   # largest prime
    g = generator(p)
    steps = []
    for _ in range(12):                          # twelve secrets for each prime
        a = rng.randrange(2, p - 1)
        found, count = brute_force(p, g, pow(g, a, p))
        assert found == a
        steps.append(count)
    mean = sum(steps) / len(steps)
    print(f"{bits} bits: p = {p:>8}, g = {g:>2}, mean steps {mean:>9.0f}"
          f" = {mean / p:.2f} p")
