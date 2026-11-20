"""otp.py -- the one-time pad, and what happens when its key is used twice."""

import random


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


rng = random.Random(27)  # a fixed seed so the run repeats; a real pad uses secrets
m1 = b"MEET AT THE LIBRARY AT NOON"
m2 = b"THE KEY IS UNDER THE MAT   "
key = rng.randbytes(len(m1))
c1, c2 = xor(m1, key), xor(m2, key)
print("c1:", c1.hex())
print("decrypted:", xor(c1, key).decode())
fake = b"STAY HOME, THE PLAN IS OFF "  # any 27 bytes: some key gives them
print("the key", xor(c1, fake).hex(), "decrypts c1 to", xor(c1, xor(c1, fake)).decode())
x = xor(c1, c2)
print("c1 xor c2 = m1 xor m2:", x.hex(), x == xor(m1, m2))
for guess in (b"THE ", b"LIBRARY"):  # guess a word of m1 at every position
    for i in range(len(x) - len(guess) + 1):
        piece = xor(x[i : i + len(guess)], guess)
        if all(65 <= b <= 90 or b == 32 for b in piece):
            print(
                f"m1 has {guess.decode()!r} at {i:>2}? then m2 has {piece.decode()!r}"
            )
