"""Grade 9, chapter 3: grids and images."""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"
sys.path.insert(0, str(LISTINGS))

from blur import blur  # noqa: E402
from pgm import pgm_text, read_pgm  # noqa: E402

SHAPE = read_pgm(LISTINGS / "shape.pgm")


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_shape_file_is_regenerated_identically(tmp_path):
    before = (LISTINGS / "shape.pgm").read_text()
    subprocess.run([sys.executable, str(HERE / "figures" / "make_shape.py")], check=True)
    assert (LISTINGS / "shape.pgm").read_text() == before
    assert len(SHAPE) == 12 and len(SHAPE[0]) == 16
    assert max(len(line) for line in before.splitlines()) <= 70


def test_round_trip_and_changes():
    path = HERE / "outputs"
    assert read_pgm(LISTINGS / "shape.pgm") == SHAPE
    text = pgm_text(SHAPE)
    assert text.split()[:4] == ["P2", "16", "12", "255"]
    neg = (path / "negative.txt").read_text().split("\n", 1)[1]
    assert [int(w) for w in neg.split()[4:]] == [255 - v for row in SHAPE for v in row]
    blurred = blur(SHAPE)
    assert blurred[0][0] == round((40 * 3 + 40) / 4)
    assert all(0 <= v <= 255 for row in blurred for v in row)


def test_spread():
    lines = (HERE / "outputs" / "spread.txt").read_text().splitlines()
    for k in range(1, 7):
        assert f"after  {k} blurs: {(2 * k + 1) ** 2:>3} cells lit" in lines[1 + k]


def test_exercises():
    grid = [[3, 8, 1, 6], [7, 2, 9, 4], [5, 0, 4, 2]]
    assert grid[2][0] == 5
    assert load("exercises", "transpose").transpose(grid)[0] == [3, 7, 5]
    try:
        load("exercises", "neighbours_bug").neighbours4(grid, 2, 3)
        raise AssertionError("should read outside")
    except IndexError:
        pass
    assert load("exercises", "neighbours_bug").neighbours4(grid, 0, 0) == [5, 7, 6, 8]
    assert sorted(load("exercises", "neighbours_fixed").neighbours4(grid, 0, 0)) == [7, 8]
    assert load("exercises", "mirror_bug").mirror(grid)[0] == [5, 0, 4, 2]
    assert load("exercises", "brighter").brighter([[250, 3]], -10) == [[240, 0]]
    assert load("exercises", "brighter").brighter([[250, 3]], 10) == [[255, 13]]
    rot = load("exercises", "rotate").rotate(grid)
    assert rot == [[5, 7, 3], [0, 2, 8], [4, 9, 1], [2, 4, 6]]
    thr = [[255 if v >= 128 else 0 for v in row] for row in SHAPE]
    assert load("exercises", "count_white").count_white(thr) == sum(
        v >= 128 for row in SHAPE for v in row)
    life = load("exercises", "life").step
    blinker = [[0] * 5 for _ in range(5)]
    for c in [1, 2, 3]:
        blinker[2][c] = 1
    turned = life(blinker)
    assert [turned[r][2] for r in range(5)] == [0, 1, 1, 1, 0] and sum(map(sum, turned)) == 3
    assert life(turned) == blinker
    four = sum(len(load("exercises", "neighbours_fixed").neighbours4(
        [[0] * 5 for _ in range(4)], r, c)) for r in range(4) for c in range(5))
    assert four == 2 * (4 * 4 + 5 * 3)
