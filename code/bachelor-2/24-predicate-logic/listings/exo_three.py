"""exo_three.py: one sentence, three structures."""
from formulas import parse
from structures import Structure

SENTENCES = ["forall x. exists y. R(x, y)", "~(exists x. R(x, x))",
             "exists y. forall x. ~R(x, y)"]
STRUCTURES = {
    "Z/3, R(x, y) when y = x + 1": Structure(range(3), {"R": {(0, 1), (1, 2), (2, 0)}}),
    "{0, 1, 2}, R(x, y) when x < y":
        Structure(range(3), {"R": {(0, 1), (0, 2), (1, 2)}}),
    "{0, 1}, R(x, y) when x != y": Structure(range(2), {"R": {(0, 1), (1, 0)}}),
}
for name, A in STRUCTURES.items():
    print(f"{name:31}", "  ".join(str(A.holds(parse(s))) for s in SENTENCES))
