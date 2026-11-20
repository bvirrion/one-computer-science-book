"""fit_copy.py: fit t = a * reads + c * n to the measured copy times (exercise 11)."""
from pathlib import Path

N = 4 << 20                                       # bytes copied in buffered_vs_raw.c
rows = []
for line in Path("../outputs/buffered_vs_raw.txt").read_text().splitlines()[2:]:
    if not line.startswith("putc"):
        b, reads, ms = line.split()
        rows.append((int(b), int(reads), float(ms)))

# least squares on relative errors: minimise the sum of ((a x + c N - t) / t)^2
s = [[0.0, 0.0], [0.0, 0.0]]
r = [0.0, 0.0]
for _, x, t in rows:
    u, v = x / t, N / t
    s[0][0] += u * u
    s[0][1] += u * v
    s[1][1] += v * v
    r[0] += u
    r[1] += v
det = s[0][0] * s[1][1] - s[0][1] ** 2
a = (r[0] * s[1][1] - r[1] * s[0][1]) / det
c = (r[1] * s[0][0] - r[0] * s[0][1]) / det
print(f"a = {a * 1e6:.0f} ns per read and write, c = {c * 1e6:.3f} ns per byte")
for b, x, t in rows:
    print(f"b = {b:>5}: measured {t:7.1f} ms, model {a * x + c * N:7.1f} ms")
