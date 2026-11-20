"""Exercise 12: Poly1305 (RFC 8439, section 2.5): a one-time authenticator. The
16-byte blocks of the message, each with a 1 byte appended, are the coefficients of a
polynomial evaluated at r modulo 2^130 - 5; s is added at the end."""


def poly1305(key, msg):
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF  # clamp
    s = int.from_bytes(key[16:], "little")
    p, acc = 2**130 - 5, 0
    for i in range(0, len(msg), 16):
        n = int.from_bytes(msg[i : i + 16] + b"\x01", "little")
        acc = (acc + n) * r % p
    return ((acc + s) % 2**128).to_bytes(16, "little")


if __name__ == "__main__":
    key = bytes.fromhex(
        "85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b"
    )
    tag = poly1305(key, b"Cryptographic Forum Research Group")
    print(tag.hex(), tag.hex() == "a8061dc1305136c6c22b8baf0c0127a9")
