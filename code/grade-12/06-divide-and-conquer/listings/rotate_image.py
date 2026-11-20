"""Read a PGM picture, turn it a quarter by quadrants, write it back."""
import tempfile
from pathlib import Path

from rotate_copy import rotate_copy
from rotate_quadrants import rotate_in_place


def read_pgm(path):
    words = Path(path).read_text().split()
    width, height = int(words[1]), int(words[2])
    values = [int(w) for w in words[4:]]
    return [values[r * width:(r + 1) * width] for r in range(height)]


def write_pgm(path, grid):
    rows = "\n".join(" ".join(str(v) for v in row) for row in grid)
    Path(path).write_text(f"P2\n{len(grid[0])} {len(grid)}\n255\n{rows}\n")


def as_text(grid):
    return ["".join("#" if v < 100 else ("+" if v < 200 else ".") for v in row)
            for row in grid]


picture = read_pgm("arrow.pgm")
turned = [row[:] for row in picture]
rotate_in_place(turned)
with tempfile.TemporaryDirectory() as folder:
    write_pgm(Path(folder) / "arrow_turned.pgm", turned)
    again = read_pgm(Path(folder) / "arrow_turned.pgm")
for before, after in zip(as_text(picture), as_text(again)):
    print(before, "  ", after)
print("same as the copy:", again == rotate_copy(picture), "| pixel sum:",
      sum(map(sum, picture)), sum(map(sum, again)))
