"""rsa.py -- textbook RSA with Python's integers. For understanding only: textbook RSA
is deterministic and malleable, and a real system uses a vetted library with OAEP
padding for encryption and PSS for signatures."""

from math import gcd

from groups import random_prime

E = 65537


def keygen(bits, rng):
    """Two random primes of bits/2 bits each, with e = 65537 invertible mod phi(n)."""
    while True:
        p, q = random_prime(bits // 2, rng), random_prime(bits // 2, rng)
        phi = (p - 1) * (q - 1)
        if p != q and gcd(E, phi) == 1 and (p * q).bit_length() == bits:
            d = pow(E, -1, phi)  # e d = 1 mod phi(n)
            return {"n": p * q, "e": E}, {"n": p * q, "d": d, "p": p, "q": q}


def encrypt(pub, m):
    assert 0 <= m < pub["n"]
    return pow(m, pub["e"], pub["n"])  # c = m^e mod n


def decrypt(priv, c):
    return pow(c, priv["d"], priv["n"])  # m = c^d mod n


def power(b, e, n, count):
    """Square and multiply, counting the products in count[0]."""
    r = 1
    for bit in bin(e)[2:]:
        r = r * r % n
        count[0] += 1
        if bit == "1":
            r = r * b % n
            count[0] += 1
    return r
