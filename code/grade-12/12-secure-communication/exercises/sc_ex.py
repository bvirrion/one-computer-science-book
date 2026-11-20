"""Exercises of the chapter on cryptography and secure communication."""
import hashlib
import hmac
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from mini_rsa import apply, digest_number  # noqa: E402
from xor_stream import key_stream  # noqa: E402


def xor_bytes(a, b):                                       # exercise 5
    if len(a) != len(b):
        raise ValueError("the two byte strings must have the same length")
    return bytes(x ^ y for x, y in zip(a, b))


def encrypt_with_nonce(key, nonce, message):               # exercise 6: the fix
    """A fresh number per message gives a fresh key stream."""
    return xor_bytes(message, key_stream(f"{key}:{nonce}", len(message)))


def dh_shared(p, a, B):                                    # exercise 7
    return pow(B, a, p)


def verify_wrong(public, message, signature):              # exercise 9: the fault
    number = int.from_bytes(message.encode(), "big") % public[0]
    return apply(public, signature) == number


def verify_right(public, message, signature):
    return apply(public, signature) == digest_number(message, public[0])


def encrypt_text(public, text):                            # exercise 11
    """Each byte encrypted on its own: the same byte always gives the same number."""
    return [apply(public, byte) for byte in text.encode()]


def store_password(password, rounds=600_000):              # exercise 14
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    return salt, rounds, digest


def check_password(stored, attempt):
    salt, rounds, digest = stored
    trial = hashlib.pbkdf2_hmac("sha256", attempt.encode(), salt, rounds)
    return hmac.compare_digest(trial, digest)


def mitm(p, g, a, b, m):                                   # exercise 15
    """Mallory replaces A and B by her own share: two secrets, both known to her."""
    A, B, M = pow(g, a, p), pow(g, b, p), pow(g, m, p)
    alice, bob = pow(M, a, p), pow(M, b, p)                # each received M
    return (alice, pow(A, m, p)), (bob, pow(B, m, p))
