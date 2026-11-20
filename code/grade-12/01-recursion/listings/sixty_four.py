"""The legend's tower: 64 disks, one move per second."""
from hanoi import hanoi

for n in range(1, 11):                       # check the formula on small towers
    moves = []
    hanoi(n, "A", "C", "B", moves)
    assert len(moves) == 2**n - 1
moves_64 = 2**64 - 1
year = 365.25 * 24 * 3600                    # seconds in a year, on average
print(f"moves for 64 disks: {moves_64:,}")
print(f"seconds in a year: {year:,.0f}")
print(f"years at one move per second: {moves_64 / year:,.0f}")
print(f"about {moves_64 / year / 1e9:.0f} billion years")
