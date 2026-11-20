"""resolver_cache.py: how many queries a cache answers, for a rate and a lifetime."""
import random


def hit_fraction(rate, lifetime, n=200_000, seed=1):
    """Queries arrive at random (rate per second); a miss caches for lifetime s."""
    rng, now, expires, hits = random.Random(seed), 0.0, -1.0, 0
    for _ in range(n):
        now += rng.expovariate(rate)             # time to the next query
        if now < expires:
            hits += 1                            # answered from the cache
        else:
            expires = now + lifetime             # asked upstream, kept for lifetime
    return hits / n


print(" queries/s  lifetime   simulated   rT/(1 + rT)")
for rate, lifetime in ((1 / 600, 3600), (1 / 60, 3600), (1, 3600), (1 / 60, 60),
                       (1, 60), (100, 60)):
    rt = rate * lifetime
    print(f"{rate:10.4f} {lifetime:7d} s   {hit_fraction(rate, lifetime):9.4f}"
          f"   {rt / (1 + rt):11.4f}")
