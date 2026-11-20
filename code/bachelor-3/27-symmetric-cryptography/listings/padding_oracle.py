"""padding_oracle.py -- a toy service decrypts AES-CBC messages and answers "bad
padding" or "ok". That one bit is enough to decrypt any message, without the key.
Then the service checks an HMAC over the ciphertext before decrypting, and the
attack learns nothing."""

import hashlib
import hmac
import random

from modes import cbc_decrypt, cbc_encrypt, pad, unpad

rng = random.Random(27)
KEY, MAC_KEY = rng.randbytes(16), rng.randbytes(16)
queries = 0


def service(iv, c):
    """Decrypt and say whether the padding was right: the oracle."""
    global queries
    queries += 1
    try:
        unpad(cbc_decrypt(KEY, iv, c))
        return True
    except ValueError:
        return False


def attack_block(oracle, prev, block):
    """Find D(block) byte by byte from the end, by forging the block before it."""
    d = bytearray(16)  # D(block), the block cipher's output before the XOR
    for k in range(1, 17):  # make the last k bytes decrypt to the padding k
        for guess in range(256):
            fake = bytearray(16)
            for j in range(16 - k + 1, 16):
                fake[j] = d[j] ^ k
            fake[16 - k] = guess
            if oracle(bytes(fake), block):
                if k == 1:  # rule out a longer padding that happened to be valid
                    fake[14] ^= 1
                    if not oracle(bytes(fake), block):
                        continue
                d[16 - k] = guess ^ k
                break
    return bytes(x ^ y for x, y in zip(d, prev))


def attack(oracle, iv, c):
    prevs = [iv] + [c[i : i + 16] for i in range(0, len(c) - 16, 16)]
    blocks = [c[i : i + 16] for i in range(0, len(c), 16)]
    return b"".join(attack_block(oracle, p, b) for p, b in zip(prevs, blocks))


secret = b"LOAN 42 TO READER 7 UNTIL 2026-12-01"
iv = rng.randbytes(16)
c = cbc_encrypt(KEY, iv, pad(secret))
found = attack(service, iv, c)
print(f"ciphertext: {len(c)} bytes; attack made {queries:,} queries")
print("recovered:", unpad(found))


def safe_service(iv, c, t):
    """Encrypt-then-MAC: reject any ciphertext whose tag is wrong, before decrypting."""
    global queries
    queries += 1
    if not hmac.compare_digest(hmac.new(MAC_KEY, iv + c, hashlib.sha256).digest(), t):
        return False
    unpad(cbc_decrypt(KEY, iv, c))
    return True


t = hmac.new(MAC_KEY, iv + c, hashlib.sha256).digest()
queries = 0
found = attack(lambda fake, block: safe_service(fake, block, t), iv, c)
print(f"against encrypt-then-MAC: {queries:,} queries, all refused")
print("bytes 'recovered':", found[:16].hex(), "... noise")
