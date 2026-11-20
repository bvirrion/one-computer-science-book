"""Write listings/shape.pgm, the 16 x 12 grey-level image the chapter's programs read.

    python code/grade-9/03-grids-and-images/figures/make_shape.py

A dark background (40), a grey square (120) and a white arrow pointing right (230).
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 16, 12


def value(r, c):
    if 2 <= r <= 4 and 1 <= c <= 3:
        return 120                                  # the grey square
    if 5 <= r <= 7 and 3 <= c <= 9:
        return 230                                  # the shaft of the arrow
    if 10 <= c <= 14 and abs(r - 6) <= 14 - c:
        return 230                                  # the head of the arrow
    return 40


lines = ["P2", f"{WIDTH} {HEIGHT}", "255"]
for r in range(HEIGHT):
    lines.append(" ".join(f"{value(r, c):>3}" for c in range(WIDTH)))
(HERE.parent / "listings" / "shape.pgm").write_text("\n".join(lines) + "\n")
