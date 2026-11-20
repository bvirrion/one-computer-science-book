"""aes.py -- AES-128 as FIPS 197 specifies it, written for reading, not for speed or
for use: a real program calls a vetted library, whose code also runs in constant time.
The state is 16 bytes in column order: byte r + 4c is row r, column c."""

from functools import lru_cache


def xtime(a):
    """Multiply by x in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1."""
    a <<= 1
    return a ^ 0x11B if a & 0x100 else a


def gmul(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        a, b = xtime(a), b >> 1
    return p


def inverse(a):
    """a^254 = a^-1 for a != 0, and 0 for 0."""
    r = 1
    for _ in range(254):
        r = gmul(r, a)
    return r


def affine(b):
    """FIPS 197, 5.1.1: bit i is b_i ^ b_i+4 ^ b_i+5 ^ b_i+6 ^ b_i+7 ^ c_i, c = 0x63."""
    out = 0
    for i in range(8):
        bit = (
            b >> i
            ^ b >> (i + 4) % 8
            ^ b >> (i + 5) % 8
            ^ b >> (i + 6) % 8
            ^ b >> (i + 7) % 8
            ^ 0x63 >> i
        ) & 1
        out |= bit << i
    return out


SBOX = [affine(inverse(a)) for a in range(256)]
INV_SBOX = [SBOX.index(x) for x in range(256)]


def sub_bytes(s, box=SBOX):
    return [box[b] for b in s]


def shift_rows(s, sign=1):
    """Row r moves r places to the left (sign=-1: to the right)."""
    return [s[r + 4 * ((c + sign * r) % 4)] for c in range(4) for r in range(4)]


def mix_columns(s, m=(2, 3, 1, 1)):
    out = []
    for c in range(4):
        col = s[4 * c : 4 * c + 4]
        for r in range(4):
            out.append(
                gmul(m[0], col[r])
                ^ gmul(m[1], col[(r + 1) % 4])
                ^ gmul(m[2], col[(r + 2) % 4])
                ^ gmul(m[3], col[(r + 3) % 4])
            )
    return out


def add_round_key(s, k):
    return [a ^ b for a, b in zip(s, k)]


@lru_cache
def round_keys(key):
    """Key expansion: 44 words of 4 bytes, read as 11 round keys of 16 bytes."""
    w = [list(key[4 * i : 4 * i + 4]) for i in range(4)]
    rcon = 1
    for i in range(4, 44):
        t = w[i - 1]
        if i % 4 == 0:
            t = [SBOX[b] for b in t[1:] + t[:1]]  # RotWord, then SubWord
            t[0] ^= rcon
            rcon = xtime(rcon)
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return [sum(w[4 * r : 4 * r + 4], []) for r in range(11)]


def encrypt_block(key, block):
    k = round_keys(key)
    s = add_round_key(list(block), k[0])
    for r in range(1, 11):
        s = shift_rows(sub_bytes(s))
        if r < 10:  # the last round has no MixColumns
            s = mix_columns(s)
        s = add_round_key(s, k[r])
    return bytes(s)


def decrypt_block(key, block):
    k = round_keys(key)
    s = add_round_key(list(block), k[10])
    for r in range(9, -1, -1):
        s = sub_bytes(shift_rows(s, -1), INV_SBOX)
        s = add_round_key(s, k[r])
        if r > 0:
            s = mix_columns(s, (14, 11, 13, 9))
    return bytes(s)
