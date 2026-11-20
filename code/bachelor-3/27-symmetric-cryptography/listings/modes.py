"""modes.py -- AES-128 in the modes of NIST SP 800-38A, with PKCS#7 padding. For
reading, not for use."""

from aes import decrypt_block, encrypt_block

B = 16  # block size in bytes


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def pad(m):
    """Add n bytes of value n, 1 <= n <= 16, to reach a multiple of 16."""
    n = B - len(m) % B
    return m + bytes([n]) * n


def unpad(m):
    n = m[-1] if m else 0
    if not 1 <= n <= B or m[-n:] != bytes([n]) * n:
        raise ValueError("bad padding")
    return m[:-n]


def blocks(m):
    return [m[i : i + B] for i in range(0, len(m), B)]


def ecb_encrypt(key, m):
    return b"".join(encrypt_block(key, p) for p in blocks(m))


def cbc_encrypt(key, iv, m):
    out, prev = [], iv
    for p in blocks(m):
        prev = encrypt_block(key, xor(p, prev))  # C_i = E(P_i xor C_i-1), C_0 = IV
        out.append(prev)
    return b"".join(out)


def cbc_decrypt(key, iv, c):
    out, prev = [], iv
    for x in blocks(c):
        out.append(xor(decrypt_block(key, x), prev))  # P_i = D(C_i) xor C_i-1
        prev = x
    return b"".join(out)


def ctr(key, counter, m):
    """Encryption and decryption alike: XOR with E(counter), E(counter + 1), ..."""
    n, out = int.from_bytes(counter, "big"), []
    for i, p in enumerate(blocks(m)):
        ks = encrypt_block(key, ((n + i) % 2**128).to_bytes(B, "big"))
        out.append(xor(p, ks))
    return b"".join(out)
