"""Exercise 12: HKDF (RFC 5869) with HMAC-SHA-256. Extract concentrates the entropy
of the input keying material into a pseudorandom key; Expand stretches it into as
many output bytes as needed, bound to a context string `info`."""

import hashlib
import hmac


def extract(salt, ikm):
    return hmac.new(salt or bytes(32), ikm, hashlib.sha256).digest()  # PRK


def expand(prk, info, length):
    if length > 255 * 32:
        raise ValueError("at most 255 blocks")
    t, okm, i = b"", b"", 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()  # T(i)
        okm += t
        i += 1
    return okm[:length]


def hkdf(salt, ikm, info, length):
    return expand(extract(salt, ikm), info, length)
