"""chacha20.py -- the ChaCha20 stream cipher of RFC 8439, checked on its test vectors
(sections 2.3.2 and 2.4.2)."""

import struct

M = 0xFFFFFFFF


def rotl(x, n):
    return (x << n | x >> (32 - n)) & M


def quarter_round(s, a, b, c, d):
    s[a] = (s[a] + s[b]) & M
    s[d] = rotl(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & M
    s[b] = rotl(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & M
    s[d] = rotl(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & M
    s[b] = rotl(s[b] ^ s[c], 7)


def block(key, counter, nonce):
    """64 bytes of keystream from a 32-byte key, a 32-bit counter, a 12-byte nonce."""
    const = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)  # "expand 32-byte k"
    init = [*const, *struct.unpack("<8L", key), counter, *struct.unpack("<3L", nonce)]
    s = init.copy()
    for _ in range(10):  # 20 rounds: a column round and a diagonal round, ten times
        for q in (
            (0, 4, 8, 12),
            (1, 5, 9, 13),
            (2, 6, 10, 14),
            (3, 7, 11, 15),
            (0, 5, 10, 15),
            (1, 6, 11, 12),
            (2, 7, 8, 13),
            (3, 4, 9, 14),
        ):
            quarter_round(s, *q)
    return struct.pack("<16L", *((x + y) & M for x, y in zip(s, init)))


def chacha20(key, counter, nonce, data):
    out = bytearray()
    for i in range(0, len(data), 64):
        ks = block(key, counter + i // 64, nonce)
        out += bytes(x ^ y for x, y in zip(data[i : i + 64], ks))
    return bytes(out)


if __name__ == "__main__":
    key = bytes(range(32))
    got = block(key, 1, bytes.fromhex("000000090000004a00000000"))
    print(
        "block 2.3.2:",
        got.hex()[:32],
        "...",
        got.hex()
        == (
            "10f1e7e4d13b5915500fdd1fa32071c4c7d1f4c733c068030422aa9ac3d46c4e"
            "d2826446079faa0914c2d705d98b02a2b5129cd1de164eb9cbd083e8a2503c4e"
        ),
    )
    plain = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you only"
        b" one tip for the future, sunscreen would be it."
    )
    c = chacha20(key, 1, bytes.fromhex("000000000000004a00000000"), plain)
    print(
        "cipher 2.4.2:",
        c.hex()[:32],
        "...",
        c.hex()
        == (
            "6e2e359a2568f98041ba0728dd0d6981e97e7aec1d4360c20a27afccfd9fae0b"
            "f91b65c5524733ab8f593dabcd62b3571639d624e65152ab8f530c359f0861d8"
            "07ca0dbf500d6a6156a38e088a22b65e52bc514d16ccf806818ce91ab7793736"
            "5af90bbf74a35be6b40b8eedf2785e42874d"
        ),
    )
