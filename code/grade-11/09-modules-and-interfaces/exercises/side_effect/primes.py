"""Prime numbers below a million: the list is computed at import."""
print("computing the primes below 1000000...")
LIMIT = 1_000_000
sieve = [True] * LIMIT
sieve[0] = sieve[1] = False
for i in range(2, LIMIT):
    if sieve[i]:
        for j in range(i * i, LIMIT, i):
            sieve[j] = False
PRIMES = [i for i in range(LIMIT) if sieve[i]]


def is_prime(n):
    """Return True when n, below LIMIT, is prime."""
    return sieve[n]
