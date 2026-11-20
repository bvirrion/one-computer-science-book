"""attractor.py: the matches game solved backwards, then a small game with draws."""
from games import attractor

# 21 matches; a move takes 1, 2 or 3; whoever takes the last match wins. A position
# is (matches left, player to move); with no match left, the player to move has lost.
owner, succ = {}, {}
for k in range(22):
    for p in "AB":
        owner[(k, p)] = p
        other = "B" if p == "A" else "A"
        succ[(k, p)] = [(k - t, other) for t in (1, 2, 3) if t <= k]
win_a, strat = attractor(owner, succ, [(0, "B")], "A")
wins = [k for k in range(22) if (k, "A") in win_a]
print("A, to move, wins with k matches left for k =", " ".join(map(str, wins)))
print("A's winning move from 21:", f"take {21 - strat[(21, 'A')][0]};",
      "moves of both players until the end:", win_a[(21, "A")])

# A small game: circles belong to player 0, squares to player 1.
OWNER = {"a": 0, "b": 1, "c": 0, "d": 1, "e": 0, "f": 1, "g": 0, "h": 1}
SUCC = {"a": ["b", "c"], "b": ["a", "h"], "c": ["d", "e"], "d": ["e", "f"],
        "e": ["e"], "f": ["g"], "g": ["f", "h"], "h": ["h"]}
w0, s0 = attractor(OWNER, SUCC, ["e"], 0)
w1, _ = attractor(OWNER, SUCC, ["h"], 1)
print("player 0 forces e from", sorted(w0.items()), "strategy", sorted(s0.items()))
print("player 1 forces h from", sorted(w1.items()))
print("neither:", sorted(set(OWNER) - set(w0) - set(w1)))
