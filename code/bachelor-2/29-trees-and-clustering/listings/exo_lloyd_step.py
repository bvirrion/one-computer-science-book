"""exo_lloyd_step.py: one iteration of Lloyd's algorithm on the twelve points, from
the centres A, E and I."""
from dataset import small_points
from kmeans import assign, centroid, cost

PTS, NAMES = small_points(), "ABCDEFGHIJKL"
centres = [PTS[0], PTS[4], PTS[8]]
a = assign(PTS, centres)
print("assignment:", " ".join(f"{n}{j + 1}" for n, j in zip(NAMES, a)),
      f"| cost {cost(PTS, centres, a):.2f}")
new = [centroid([p for p, j in zip(PTS, a) if j == i]) for i in range(3)]
print("new centres:", " ".join(f"({x:.2f}, {y:.2f})" for x, y in new),
      f"| cost {cost(PTS, new, a):.2f}")
b = assign(PTS, new)
print("next assignment:", " ".join(f"{n}{j + 1}" for n, j in zip(NAMES, b)),
      f"| cost {cost(PTS, new, b):.2f}")
