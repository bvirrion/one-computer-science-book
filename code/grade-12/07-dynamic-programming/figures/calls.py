"""Write calls.dat: calls of the naive and of the memoised Fibonacci, n = 1 to 35."""
from pathlib import Path

naive = {0: 1, 1: 1}
for n in range(2, 36):
    naive[n] = 1 + naive[n - 1] + naive[n - 2]      # one call, plus the two below
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n naive memo\n")
    for n in range(1, 36):
        out.write(f"{n} {naive[n]} {2 * n - 1}\n")
