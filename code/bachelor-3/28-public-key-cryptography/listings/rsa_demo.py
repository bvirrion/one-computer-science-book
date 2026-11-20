"""rsa_demo.py -- a 2048-bit RSA key from a seeded generator, a round trip, and the
cost of decryption with and without the Chinese remainder theorem."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from ex6_crt import decrypt_crt  # noqa: E402
from rsa import decrypt, encrypt, keygen, power  # noqa: E402

rng = random.Random(28)
pub, priv = keygen(2048, rng)
print("n has", pub["n"].bit_length(), "bits; e =", pub["e"])
m = int.from_bytes(b"meet at the town hall at noon", "big")
c = encrypt(pub, m)
print("c starts", hex(c)[:18], "...")
print("decrypted:", decrypt(priv, c).to_bytes(29, "big").decode())
print("with the CRT:", decrypt_crt(priv, c) == m)


def cost(bits, products):  # schoolbook product of b-bit numbers: (b/64)^2 word products
    return products * (bits // 64) ** 2


full, half = [0], [0]
power(c, priv["d"], pub["n"], full)
decrypt_crt(priv, c, lambda b, e, n: power(b, e, n, half))
print(f"direct: {full[0]:,} products mod n: {cost(2048, full[0]):,} word products")
print(f"CRT:    {half[0]:,} products mod p, q: {cost(1024, half[0]):,} word products")
print(f"ratio {cost(2048, full[0]) / cost(1024, half[0]):.2f}")
