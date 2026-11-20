"""How big do the tables get? Cells of an n x m table, and of two rows."""
import sys

row = [0] * 1001
print("one list of 1001 numbers:", sys.getsizeof(row), "bytes: 8 per cell, plus 56")
print(f"{'n = m':>8} {'cells (n+1)^2':>18} {'bytes, 8 each':>18} {'two rows':>9}")
for n in [10, 100, 1000, 10_000, 100_000, 1_000_000]:
    cells = (n + 1) * (n + 1)
    print(f"{n:8} {cells:18,} {8 * cells:18,} {2 * (n + 1):9,}")
