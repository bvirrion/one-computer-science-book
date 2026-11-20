"""Turn the image and the captured outputs of the four changes into .dat grids.

    python code/grade-9/03-grids-and-images/figures/draw_images.py

Each .dat file has one line per pixel, x y grey, rows from the top, for a pgfplots
matrix plot. The pictures of the chapter are therefore drawn from the very text the
listings printed.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent


def grid_of(text):
    words = text.split()
    start = words.index("P2")
    width, height = int(words[start + 1]), int(words[start + 2])
    values = [int(w) for w in words[start + 4:start + 4 + width * height]]
    return [values[r * width:(r + 1) * width] for r in range(height)]


def write_dat(name, grid):
    lines = ["x y v"]
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            lines.append(f"{c} {r} {value}")
        lines.append("")
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / f"{name}.dat").write_text("\n".join(lines))


write_dat("shape", grid_of((CHAPTER / "listings" / "shape.pgm").read_text()))
for name in ["negative", "mirror", "threshold", "blur"]:
    write_dat(name, grid_of((CHAPTER / "outputs" / f"{name}.txt").read_text()))
