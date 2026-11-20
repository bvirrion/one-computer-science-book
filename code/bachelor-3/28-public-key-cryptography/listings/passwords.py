"""passwords.py -- storing passwords: a random salt per account and a slow,
memory-hard hash (scrypt); verifying in constant time. Then guesses per second for
an attacker who stole the table, with a fast hash and with two slow ones, measured
on one core."""

import hashlib
import hmac
import secrets
import time

N, R, PAR = 2**14, 8, 1  # scrypt cost: 2^14 x 128 x 8 bytes = 16 MiB of memory


def store(password):
    salt = secrets.token_bytes(16)
    h = hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=PAR, dklen=32)
    return salt, h


def check(password, record):
    salt, h = record
    guess = hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=PAR, dklen=32)
    return hmac.compare_digest(guess, h)  # takes the same time wherever they differ


ada, bob = store("correct horse"), store("correct horse")
print("same password, same stored hash:", ada[1] == bob[1])
print("check right / wrong:", check("correct horse", ada), check("correct house", ada))


def rate(f, guesses):
    best = min(timed(f, guesses) for _ in range(3))
    return guesses / best


def timed(f, guesses):
    t = time.perf_counter()
    for i in range(guesses):
        f(b"guess%d" % i)
    return time.perf_counter() - t


salt = bytes(16)
fast = rate(lambda pw: hashlib.sha256(salt + pw).digest(), 200_000)
pbkdf2 = rate(lambda pw: hashlib.pbkdf2_hmac("sha256", pw, salt, 600_000), 5)
scrypt = rate(lambda pw: hashlib.scrypt(pw, salt=salt, n=N, r=R, p=PAR), 20)
print(f"SHA-256 once:              {fast:12,.0f} guesses per second")
print(f"PBKDF2, 600,000 rounds:    {pbkdf2:12,.1f} guesses per second")
print(f"scrypt, n = 2^14, r = 8:   {scrypt:12,.1f} guesses per second")
print(f"slowdown: PBKDF2 {fast / pbkdf2:,.0f}x, scrypt {fast / scrypt:,.0f}x")
