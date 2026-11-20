import math

for count in (10, 1_000_000):
    tenths = [0.1] * count
    total = 0.0
    for t in tenths:
        total = total + t
    print(f"{count} tenths: loop {total!r}  fsum {math.fsum(tenths)!r}")

print(1e16 + 1.0 - 1e16, 1e16 - 1e16 + 1.0)
