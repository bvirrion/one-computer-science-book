"""SHA-256: a fixed-size digest, and a small change that changes everything."""
import hashlib

messages = ["Pay Bea 20", "Pay Bea 21", "Pay Bea 20.", "x" * 10_000]
digests = [hashlib.sha256(m.encode()).hexdigest() for m in messages]
for m, d in zip(messages, digests):
    print(f"{m[:12]:12} ({len(m):5} characters): {d[:32]}...")
print("every digest has", len(digests[0]) * 4, "bits")


def bits_differ(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count("1")


print("bits that differ between the first two:", bits_differ(digests[0], digests[1]))
print("between the first and the third:", bits_differ(digests[0], digests[2]))
