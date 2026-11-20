"""Exercise 10: the chosen-plaintext game against CBC with a predictable IV (here the
IV of each encryption is the previous one plus 1). The attacker picks m0 and m1, gets
the encryption of one of them, then asks for one more encryption it chose so that it
equals the challenge exactly when the challenge hid m0."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from modes import cbc_encrypt, xor  # noqa: E402


class Oracle:
    def __init__(self, seed):
        rng = random.Random(seed)
        self.key, self.iv, self.b = (
            rng.randbytes(16),
            rng.randrange(2**128),
            rng.randrange(2),
        )

    def encrypt(self, m):
        self.iv = (self.iv + 1) % 2**128
        iv = self.iv.to_bytes(16, "big")
        return iv, cbc_encrypt(self.key, iv, m)


def play(seed):
    o = Oracle(seed)
    m0, m1 = bytes(16), b"\xff" * 16
    iv1, c1 = o.encrypt([m0, m1][o.b])  # the challenge
    iv2 = ((int.from_bytes(iv1, "big") + 1) % 2**128).to_bytes(16, "big")  # predicted
    _, c2 = o.encrypt(xor(xor(m0, iv1), iv2))  # E(m0 xor iv1) if b = 0
    guess = 0 if c2 == c1 else 1
    return guess == o.b


if __name__ == "__main__":
    print("attacker wins", sum(play(s) for s in range(200)), "of 200 games")
