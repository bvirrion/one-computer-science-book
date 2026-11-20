"""primality.py: the Fermat test and the Miller-Rabin test, one base at a time."""


def fermat_passes(n, a):
    """True if a^(n-1) = 1 mod n, as for every base a coprime to a prime n."""
    return pow(a, n - 1, n) == 1


def miller_rabin_passes(n, a):
    """Write n - 1 = 2^s d with d odd. A prime n passes for every base: either
    a^d = 1, or one of a^d, a^(2d), ..., a^(2^(s-1) d) is -1 mod n."""
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False  # a is a witness: n is composite


def is_probable_prime(n, rounds, rng):
    """Monte Carlo: 'composite' is always right; 'prime' is wrong with probability
    at most 4^-rounds."""
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    return all(miller_rabin_passes(n, rng.randrange(2, n - 1)) for _ in range(rounds))
