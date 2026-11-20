"""Exercise 6: CBC decryption with a padding check, written from the specification:
P_i = D(C_i) xor C_i-1 with C_0 = IV, then remove PKCS#7 padding or refuse."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from aes import decrypt_block  # noqa: E402


def cbc_decrypt_checked(key, iv, c):
    if len(iv) != 16 or not c or len(c) % 16:
        raise ValueError("ciphertext must be a non-empty multiple of 16 bytes")
    out, prev = bytearray(), iv
    for i in range(0, len(c), 16):
        block = c[i : i + 16]
        out += bytes(x ^ y for x, y in zip(decrypt_block(key, block), prev))
        prev = block
    n = out[-1]
    if not 1 <= n <= 16 or out[-n:] != bytes([n]) * n:
        raise ValueError("bad padding")
    return bytes(out[:-n])
