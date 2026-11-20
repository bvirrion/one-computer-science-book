"""Diffie-Hellman: two parties agree on a secret; a listener sees every message."""
import random

rng = random.Random(2026)                        # real code uses the secrets module


def exchange(p, g):
    a = rng.randrange(2, p - 1)                  # Alice's secret, never sent
    b = rng.randrange(2, p - 1)                  # Bob's secret, never sent
    A = pow(g, a, p)                             # Alice sends A
    B = pow(g, b, p)                             # Bob sends B
    alice = pow(B, a, p)                         # Alice computes from B and a
    bob = pow(A, b, p)                           # Bob computes from A and b
    print(f"public: p = {p}, g = {g}")
    print(f"  sent: A = {A}, B = {B}   (the listener sees these)")
    print(f"  kept: a = {a}, b = {b}")
    print(f"  Alice finds {alice}, Bob finds {bob}: same = {alice == bob}")


exchange(23, 5)
exchange(2**61 - 1, 3)                           # a prime of 61 bits
