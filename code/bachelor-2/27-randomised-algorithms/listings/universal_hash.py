"""universal_hash.py: keys chosen against h(x) = x mod m, then hashed by a function
drawn from the Carter-Wegman family after the keys are fixed."""
import random

P = 2**31 - 1  # a prime larger than every key


def draw(m, rng):
    """A random member of the family h(x) = ((a x + b) mod p) mod m."""
    a, b = rng.randrange(1, P), rng.randrange(P)
    return lambda x: (a * x + b) % P % m


def chains(keys, h, m):
    lengths = [0] * m
    for x in keys:
        lengths[h(x)] += 1
    return lengths


if __name__ == "__main__":
    rng = random.Random(7)
    print("    n  fixed: longest | universal, 1,000 draws: longest (median)"
          "  key's chain  bound")
    for n in range(200, 1001, 200):
        m = n  # load factor 1
        keys = [m * r for r in rng.sample(range(1, 10**6), n)]  # multiples of m
        fixed = chains(keys, lambda x, m=m: x % m, m)
        longest, seen = [], 0.0
        for _ in range(1000):
            univ = chains(keys, draw(m, rng), m)
            longest.append(max(univ))
            seen += sum(c * c for c in univ) / n / 1000  # chain length seen by a key
        median = sorted(longest)[500]
        bound = 1 + (n - 1) / m
        print(f"{n:5} {max(fixed):14} | {median:37} {seen:13.3f} {bound:6.3f}")
