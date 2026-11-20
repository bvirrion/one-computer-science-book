"""A toy stream cipher: xor with bytes from a seeded generator. Not secure."""
import random


def key_stream(key, n):
    """n bytes that depend only on the key: the same key gives the same bytes."""
    rng = random.Random(key)
    return bytes(rng.randrange(256) for _ in range(n))


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


if __name__ == "__main__":
    message = b"Meet at the bridge at noon"
    key = 314159                                  # the shared secret
    cipher = xor_bytes(message, key_stream(key, len(message)))
    print("message:", message.hex(" "))
    print("cipher: ", cipher.hex(" "))
    back = xor_bytes(cipher, key_stream(key, len(cipher)))
    print("decrypted with the key:  ", back.decode())
    wrong = xor_bytes(cipher, key_stream(271828, len(cipher)))
    print("decrypted with another:  ", wrong[:12].hex(" "), "...")
