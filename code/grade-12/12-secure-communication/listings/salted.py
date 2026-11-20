"""Storing passwords: a salted digest, never the password itself."""
import hashlib
import random

rng = random.Random(42)                          # real code uses secrets.token_bytes


def store(password):
    salt = bytes(rng.randrange(256) for _ in range(8))
    return salt, hashlib.sha256(salt + password.encode()).hexdigest()


def check(stored, attempt):
    salt, digest = stored
    return hashlib.sha256(salt + attempt.encode()).hexdigest() == digest


users = {"ada": store("tulip7"), "bea": store("tulip7")}   # the same password
for name, (salt, digest) in users.items():
    print(f"{name}: salt {salt.hex()}  digest {digest[:24]}...")
print("ada logs in with tulip7:", check(users["ada"], "tulip7"))
print("ada logs in with tulip8:", check(users["ada"], "tulip8"))
