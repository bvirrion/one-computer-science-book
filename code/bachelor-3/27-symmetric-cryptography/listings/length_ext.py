"""length_ext.py -- a toy service authenticates orders with tag = SHA-256(key || m).
Knowing one order and its tag, but not the key, an attacker appends to the order and
computes a valid tag. The same attack fails on HMAC."""

import hashlib
import hmac
import random
import struct

from sha256 import pad, sha256

key = random.Random(27).randbytes(16)  # the service's secret


def naive_tag(m):
    return sha256(key + m)


order = b"reader=r7&book=42&days=14"
tag = naive_tag(order)
print("order:", order.decode(), " tag:", tag.hex()[:16], "...")
# The attacker knows the order, the tag and the key's length, 16 bytes; it continues
# the hash from the tag, which is the state after key || order || padding.
glue = pad(16 + len(order))
extra = b"&days=365"
state = struct.unpack(">8L", tag)
forged_tag = sha256(extra, state, done=16 + len(order) + len(glue))
forged = order + glue + extra
print("forged order:", forged)
print("accepted by the naive service:", naive_tag(forged) == forged_tag)
good = hmac.new(key, order, hashlib.sha256).digest()
state = struct.unpack(">8L", good)
attempt = sha256(extra, state, done=64 + len(order) + len(pad(64 + len(order))))
print(
    "same trick against HMAC accepted:",
    hmac.compare_digest(hmac.new(key, forged, hashlib.sha256).digest(), attempt),
)
