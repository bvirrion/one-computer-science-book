"""The turtle drawings of grade 6, chapter 3: sides, side lengths, angles, closed or not."""

import math
import re
from pathlib import Path

from turtlerec import record, record_source, same_polygon, simplify

HERE = Path(__file__).resolve().parent.parent


def draw(folder, name):
    return record(HERE / folder / f"{name}.py")


def corners(d):
    assert len(d.strokes) == 1
    return simplify(d.strokes[0].points)


def closed(points):
    return math.dist(points[0], points[-1]) < 1e-6


def sides(points):
    return [math.dist(a, b) for a, b in zip(points, points[1:])]


def star(n, k):
    text = (HERE / "listings" / "stars.py").read_text()
    text = re.sub(r"^n = \d+", f"n = {n}", text, flags=re.M)
    return record_source(re.sub(r"^k = \d+", f"k = {k}", text, flags=re.M))


def points_visited(d):
    return {(round(x, 4) + 0.0, round(y, 4) + 0.0) for x, y in d.strokes[0].points}


def test_square_with_and_without_loop():
    long, short = draw("listings", "square_long"), draw("listings", "square")
    square = [(0, 0), (100, 0), (100, 100), (0, 100)]
    assert same_polygon(corners(long), square) and same_polygon(corners(short), square)
    assert long.moves == short.moves


def test_polygons_close_with_360_over_n():
    hexagon = corners(draw("listings", "polygon"))
    assert closed(hexagon) and len(hexagon) == 7
    assert all(abs(s - 60) < 1e-6 for s in sides(hexagon))
    for name, n, side in [("triangle", 3, 120), ("octagon", 8, 50)]:
        pts = corners(draw("exercises", name))
        assert closed(pts) and len(pts) == n + 1
        assert all(abs(s - side) < 1e-6 for s in sides(pts))
    wrong = corners(draw("exercises", "open_polygon"))
    assert not closed(wrong)
    assert abs(draw("exercises", "open_polygon").turtles[0].heading() - 300) < 1e-6


def test_star_turns_twice_round():
    d = draw("listings", "star")
    pts = corners(d)
    assert closed(pts) and len(pts) == 6
    assert all(abs(s - 150) < 1e-6 for s in sides(pts))
    assert 5 * 144 == 2 * 360


def test_spiral_sides_grow():
    d = draw("listings", "spiral")
    lengths = [s for s in sides(d.strokes[0].points) if s > 0]
    assert lengths == [5 * i for i in range(1, 40)]


def test_rows():
    d = draw("listings", "row_of_squares")
    assert len(d.strokes) == 5
    widths = [round(max(x for x, _ in s.points) - min(x for x, _ in s.points)) for s in d.strokes]
    assert widths == [20, 30, 40, 50, 60]
    d = draw("exercises", "row_of_triangles")
    assert len(d.strokes) == 1
    assert len(points_visited(d)) == 11   # 6 points on the base line, 5 tops


def test_stars_of_every_size():
    """For n points and k full turns, a single line through all n points exactly when gcd(n, k) == 1."""
    singles = {}
    for n in range(5, 13):
        singles[n] = []
        for k in range(1, n):
            d = star(n, k)
            pts = d.strokes[0].points
            assert closed(pts)
            assert abs(sum(360 * k / n for _ in range(n)) - 360 * k) < 1e-9
            if len(points_visited(d)) == n:
                singles[n].append(k)
            assert (len(points_visited(d)) == n) == (math.gcd(n, k) == 1)
    assert singles[5] == [1, 2, 3, 4]
    assert singles[8] == [1, 3, 5, 7]
    assert singles[12] == [1, 5, 7, 11]
    assert {n: len(v) for n, v in singles.items()} == {
        5: 4, 6: 2, 7: 6, 8: 4, 9: 6, 10: 4, 11: 10, 12: 4
    }
    assert len(points_visited(star(8, 2))) == 4    # a square, drawn twice
    assert len(points_visited(star(8, 4))) == 2    # a line, walked back and forth
