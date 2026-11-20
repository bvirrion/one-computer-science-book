"""sha256.py -- SHA-256 as FIPS 180-4 specifies it: pad the message, cut it into
64-byte blocks, and run the compression function on each from the initial hash value.
The constants are computed as the standard defines them."""

import struct
from math import isqrt

M = 0xFFFFFFFF


def primes(n):
    ps, k = [], 2
    while len(ps) < n:
        if all(k % p for p in ps):
            ps.append(k)
        k += 1
    return ps


def frac_bits(x):
    """The first 32 bits of the fractional part of x."""
    return int((x - int(x)) * 2**32)


def icbrt(n):  # floor of the cube root, exactly
    r = round(n ** (1 / 3))
    while r**3 > n:
        r -= 1
    while (r + 1) ** 3 <= n:
        r += 1
    return r


# the first 32 bits of the fractional parts of the cube roots of the first 64 primes,
# and of the square roots of the first 8, computed in integers to avoid rounding
K = [icbrt(p << 96) & M for p in primes(64)]
H0 = [isqrt(p << 64) & M for p in primes(8)]


def rotr(x, n):
    return (x >> n | x << (32 - n)) & M


def pad(length):
    """The padding of a message of `length` bytes: 0x80, zeros, the length in bits."""
    return b"\x80" + bytes((55 - length) % 64) + struct.pack(">Q", 8 * length)


def compress(h, chunk):
    w = list(struct.unpack(">16L", chunk))
    for t in range(16, 64):
        s0 = rotr(w[t - 15], 7) ^ rotr(w[t - 15], 18) ^ w[t - 15] >> 3
        s1 = rotr(w[t - 2], 17) ^ rotr(w[t - 2], 19) ^ w[t - 2] >> 10
        w.append((w[t - 16] + s0 + w[t - 7] + s1) & M)
    a, b, c, d, e, f, g, hh = h
    for t in range(64):
        t1 = (
            hh
            + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25))
            + (e & f ^ ~e & g)
            + K[t]
            + w[t]
        )
        t2 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + (a & b ^ a & c ^ b & c)
        a, b, c, d, e, f, g, hh = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    return [(x + y) & M for x, y in zip(h, (a, b, c, d, e, f, g, hh))]


def sha256(m, h=None, done=0):
    """Hash m; or continue from the intermediate value h reached after `done` bytes."""
    h = list(h or H0)
    data = m + pad(done + len(m))
    for i in range(0, len(data), 64):
        h = compress(h, data[i : i + 64])
    return struct.pack(">8L", *h)
