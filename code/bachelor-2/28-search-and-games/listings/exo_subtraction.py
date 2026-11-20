"""exo_subtraction.py: take 1, 3 or 4 matches; whoever takes the last wins."""
from games import attractor

N = 30
owner, succ = {}, {}
for k in range(N + 1):
    for p in "AB":
        owner[(k, p)] = p
        succ[(k, p)] = [(k - t, "B" if p == "A" else "A") for t in (1, 3, 4) if t <= k]
win, _ = attractor(owner, succ, [(0, "B")], "A")
lose = [k for k in range(N + 1) if (k, "A") not in win]
print("the player to move loses with k =", lose)
print("k mod 7 of these:", sorted({k % 7 for k in lose}))
