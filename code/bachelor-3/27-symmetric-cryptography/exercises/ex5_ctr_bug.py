"""Exercise 5: a CTR service that starts every message at counter 0 under one key,
and the fix: a fresh 8-byte nonce per message in the counter block's first half."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from modes import ctr, xor  # noqa: E402


def encrypt_buggy(key, m, nonce=None):
    return ctr(key, bytes(16), m)  # the same keystream for every message


def encrypt_fixed(key, m, nonce):
    """nonce: 8 bytes, never repeated under one key; the counter fills the rest."""
    return nonce + ctr(key, nonce + bytes(8), m)


def decrypt_fixed(key, c):
    return ctr(key, c[:8] + bytes(8), c[8:])


if __name__ == "__main__":
    key = bytes(range(16))
    m1, m2 = b"return book 42 by friday", b"the reading room is shut"
    c1, c2 = encrypt_buggy(key, m1), encrypt_buggy(key, m2)
    print("buggy: c1 xor c2 == m1 xor m2:", xor(c1, c2) == xor(m1, m2))
    d1, d2 = (
        encrypt_fixed(key, m1, b"\x00" * 7 + b"\x01"),
        encrypt_fixed(key, m2, b"\x00" * 7 + b"\x02"),
    )
    print("fixed: c1 xor c2 == m1 xor m2:", xor(d1[8:], d2[8:]) == xor(m1, m2))
    print("fixed decrypts:", decrypt_fixed(key, d1) == m1)
