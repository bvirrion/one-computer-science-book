"""sha256_check.py -- the SHA-256 of sha256.py against Python's hashlib."""

import hashlib
import random

from sha256 import H0, K, pad, sha256

print("K[0], K[63]:", f"{K[0]:08x} {K[63]:08x}", " H0[0]:", f"{H0[0]:08x}")
print('SHA-256("abc") =', sha256(b"abc").hex())
rng = random.Random(27)
msgs = [rng.randbytes(rng.randrange(0, 300)) for _ in range(1000)]
same = sum(sha256(m) == hashlib.sha256(m).digest() for m in msgs)
print(f"equal to hashlib on {same} of {len(msgs)} random messages of 0 to 299 bytes")
for n in (55, 56, 64):  # one block of padding, or two
    print(f"a message of {n} bytes is padded to {n + len(pad(n))} bytes")
