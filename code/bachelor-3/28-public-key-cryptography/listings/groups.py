"""groups.py -- primes and prime-order subgroups for the chapter's toy public-key
systems. Randomness comes from a seeded generator so that every run prints the same
numbers; a real system draws its secrets from the secrets module."""


def is_probable_prime(n, rng, rounds=40):
    """Miller--Rabin with random bases (Year 2 volume)."""
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # the base is a witness: n is composite
    return True


def random_prime(bits, rng):
    while True:
        n = rng.getrandbits(bits) | 1 << (bits - 1) | 1
        if is_probable_prime(n, rng):
            return n


def subgroup(qbits, pbits, rng):
    """A prime q of qbits bits, a prime p = kq + 1 of pbits bits, and g of order q."""
    q = random_prime(qbits, rng)
    while True:
        k = rng.getrandbits(pbits - qbits) | 1 << (pbits - qbits - 1)
        k -= k % 2  # p = kq + 1 must be odd, so k is even
        p = k * q + 1
        if p.bit_length() == pbits and is_probable_prime(p, rng):
            break
    while True:
        g = pow(rng.randrange(2, p - 1), k, p)  # an element of order 1 or q
        if g != 1:
            return p, q, g
