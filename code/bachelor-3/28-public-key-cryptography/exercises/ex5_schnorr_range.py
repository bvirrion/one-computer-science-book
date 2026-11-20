"""Exercise 5: a Schnorr verifier that skips the range check on s accepts a second
signature, (r, s + q), that the signer never produced. The fix restores the check."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from schnorr import G, P, Q, challenge, keygen, sign, verify  # noqa: E402


def verify_buggy(y, m, sig):
    r, s = sig
    return pow(G, s, P) == r * pow(y, challenge(r, m), P) % P  # no range check


if __name__ == "__main__":
    rng = random.Random(5)
    x, y = keygen(rng)
    m = b"grant 300 to the reading club"
    r, s = sign(x, m, rng)
    twin = (r, s + Q)  # g^(s + q) = g^s, since g has order q
    print("buggy verifier accepts the twin:", verify_buggy(y, m, twin))
    print("fixed verifier accepts the twin:", verify(y, m, twin))
    print("fixed verifier accepts the original:", verify(y, m, (r, s)))
