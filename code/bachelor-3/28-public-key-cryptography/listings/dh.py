"""dh.py -- Diffie--Hellman in a subgroup of prime order q (64 bits) of the integers
modulo a prime p (128 bits). Then Eve sits in the middle of the exchange."""

import hashlib
import random

from groups import subgroup

rng = random.Random(28)
p, q, g = subgroup(64, 128, rng)
print(f"p = {p}\nq = {q}\ng = {g}")


def keypair():
    x = rng.randrange(1, q)  # private
    return x, pow(g, x, p)  # public: g^x mod p


def shared(private, other_public):
    s = pow(other_public, private, p)
    return hashlib.sha256(s.to_bytes(16, "big")).hexdigest()[:16]  # derive a key


a, A = keypair()  # the town hall
b, B = keypair()  # the library
print("town hall sends A =", A)
print("library sends   B =", B)
print("town hall's key:", shared(a, B), " library's key:", shared(b, A))

e1, E1 = keypair()  # Eve replaces A by E1 on its way to the library,
e2, E2 = keypair()  # and B by E2 on its way to the town hall
print("with Eve in the middle:")
print("  town hall's key:", shared(a, E2), " Eve's key with it:", shared(e2, A))
print("  library's key:  ", shared(b, E1), " Eve's key with it:", shared(e1, B))
