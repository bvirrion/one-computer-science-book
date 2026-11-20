"""Prime numbers below a limit, computed when first needed."""
LIMIT = 1_000_000
_sieve = None


def _build():
    global _sieve
    _sieve = [True] * LIMIT
    _sieve[0] = _sieve[1] = False
    for i in range(2, LIMIT):
        if _sieve[i]:
            for j in range(i * i, LIMIT, i):
                _sieve[j] = False


def is_prime(n):
    """Return True when n, below LIMIT, is prime."""
    if _sieve is None:
        _build()
    return _sieve[n]
