"""schnorr.py -- Schnorr signatures in a subgroup of prime order q (160 bits) modulo
a prime p (1024 bits); then a signer whose random generator is stuck reuses a nonce."""

import hashlib
import random

from groups import subgroup

P, Q, G = subgroup(160, 1024, random.Random(2028))


def challenge(r, m):
    data = r.to_bytes(128, "big") + m
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def keygen(rng):
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)  # private x, public y = g^x


def sign(x, m, rng):
    k = rng.randrange(1, Q)  # a fresh secret nonce for every signature
    r = pow(G, k, P)
    e = challenge(r, m)
    return r, (k + e * x) % Q


def verify(y, m, sig):
    r, s = sig
    if not (0 <= s < Q and 1 < r < P):
        return False
    return pow(G, s, P) == r * pow(y, challenge(r, m), P) % P  # g^s = r y^e


if __name__ == "__main__":
    rng = random.Random(28)
    x, y = keygen(rng)
    sig = sign(x, b"the library may borrow the hall on 3 May", rng)
    print("valid:", verify(y, b"the library may borrow the hall on 3 May", sig))
    print("other message:", verify(y, b"the library may borrow the hall on 4 May", sig))
    stuck = random.Random(7)
    s1 = sign(x, b"pay 120 for chairs", stuck)
    stuck = random.Random(7)  # the generator restarts from the same state
    s2 = sign(x, b"pay 80 for tables", stuck)
    print("same r in both signatures:", s1[0] == s2[0])
    e1, e2 = (
        challenge(s1[0], b"pay 120 for chairs"),
        challenge(s2[0], b"pay 80 for tables"),
    )
    found = (s1[1] - s2[1]) * pow(e1 - e2, -1, Q) % Q  # k cancels out
    print("private key recovered:", found == x)
