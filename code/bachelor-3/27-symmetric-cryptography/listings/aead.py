"""aead.py -- AEAD_CHACHA20_POLY1305 (RFC 8439, section 2.8), with the Poly1305 of
exercise 12, checked on the test vector of section 2.8.2; then a tampered ciphertext."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from chacha20 import block, chacha20  # noqa: E402
from ex12_poly1305 import poly1305  # noqa: E402


def pad16(x):
    return x + bytes(-len(x) % 16)


def tag(key, nonce, aad, c):
    otk = block(key, 0, nonce)[:32]  # a fresh one-time Poly1305 key per nonce
    lengths = len(aad).to_bytes(8, "little") + len(c).to_bytes(8, "little")
    return poly1305(otk, pad16(aad) + pad16(c) + lengths)


def seal(key, nonce, aad, plain):
    c = chacha20(key, 1, nonce, plain)  # encrypt, then authenticate the ciphertext
    return c, tag(key, nonce, aad, c)


def open_(key, nonce, aad, c, t):
    if tag(key, nonce, aad, c) != t:  # check before decrypting anything
        raise ValueError("authentication failed")
    return chacha20(key, 1, nonce, c)


if __name__ == "__main__":
    key = bytes(range(0x80, 0xA0))
    nonce = bytes.fromhex("07000000") + bytes(range(0x40, 0x48))
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    plain = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you only"
        b" one tip for the future, sunscreen would be it."
    )
    c, t = seal(key, nonce, aad, plain)
    print("ciphertext starts", c[:16].hex(), c[:4].hex() == "d31a8d34")
    print("tag", t.hex(), t.hex() == "1ae10b594f09e26a7e902ecbd0600691")
    print("opens to", open_(key, nonce, aad, c, t)[:41].decode(), "...")
    forged = bytearray(c)
    forged[0] ^= 1  # flip one bit of the ciphertext
    try:
        open_(key, nonce, aad, bytes(forged), t)
    except ValueError as e:
        print("one bit flipped:", e)
