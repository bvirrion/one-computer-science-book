"""growth.py: how fast the usual cost functions grow."""

from math import log2

print(f"{'n':>4} {'log2 n':>6} {'n log2 n':>8} {'n^2':>6} {'n^3':>7} {'2^n':>20}")
for n in [2, 4, 8, 16, 32, 64]:
    print(f"{n:4d} {log2(n):6.0f} {n * log2(n):8.0f} {n**2:6d} {n**3:7d} {2**n:20d}")

n, speed = 30_000_000, 10**9  # thirty million records, a billion operations a second
for name, ops in [("n log2 n", n * log2(n)), ("n^2", n**2)]:
    seconds = ops / speed
    days = seconds / 86400
    print(f"{name:>8}: {ops:.2e} operations, {seconds:,.1f} s = {days:.2f} days")
