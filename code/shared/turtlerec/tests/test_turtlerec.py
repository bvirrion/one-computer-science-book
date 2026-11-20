import math
import subprocess
import sys
from pathlib import Path

import pytest

import turtlerec
from turtlerec import TooManyMoves, fmt, record, record_source, same_polygon, simplify

HERE = Path(__file__).resolve().parent.parent

SQUARE = """
import turtle
t = turtle.Turtle()
for i in range(4):
    t.forward(100)
    t.left(90)
turtle.done()
"""


def close(p, q, tol=1e-9):
    return math.dist(p, q) <= tol


def test_square_points_are_the_corners():
    d = record_source(SQUARE)
    assert len(d.strokes) == 1
    pts = d.strokes[0].points
    want = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    assert len(pts) == 5
    assert all(close(p, q) for p, q in zip(pts, want))
    assert same_polygon(pts, want)
    assert d.moves == 4


def test_module_level_functions_and_star_import():
    d = record_source("from turtle import *\nforward(50)\nright(90)\nforward(50)\ndone()\n")
    pts = d.strokes[0].points
    assert close(pts[-1], (50, -50))
    d2 = record_source("import turtle as t\nt.fd(30)\nt.lt(90)\nt.fd(30)\n")
    assert close(d2.strokes[0].points[-1], (30, 30))


def test_penup_splits_strokes_and_goto_draws():
    d = record_source(
        "import turtle\nt = turtle.Turtle()\nt.forward(10)\nt.penup()\nt.forward(10)\nt.pendown()\n"
        "t.forward(10)\nt.goto(0, 0)\n"
    )
    assert len(d.strokes) == 2
    assert close(d.strokes[0].points[-1], (10, 0))
    assert close(d.strokes[1].points[0], (20, 0))
    assert close(d.strokes[1].points[-1], (0, 0))


def test_circle_follows_the_standard_library_rule():
    d = record_source("import turtle\nt = turtle.Turtle()\nt.circle(50)\n")
    pts = d.strokes[0].points
    steps = 1 + int(min(11 + 50 / 6.0, 59.0))  # 20, as turtle.TNavigator.circle computes it
    assert len(pts) == steps + 1
    assert close(pts[0], pts[-1], 1e-9)
    # every corner lies on the circle of centre (0, 50) and radius 50 (an inscribed polygon)
    assert all(abs(math.dist(p, (0, 50)) - 50) < 1e-9 for p in pts)


def test_circle_steps_makes_a_regular_polygon():
    d = record_source("import turtle\nturtle.circle(40, steps=6)\n")
    pts = d.strokes[0].points
    assert len(pts) == 7
    sides = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    assert max(sides) - min(sides) < 1e-9
    assert abs(sides[0] - 40) < 1e-9  # a hexagon's side equals its circumradius


def test_colours_widths_and_new_strokes():
    d = record_source(
        "import turtle\nt = turtle.Turtle()\nt.color('red')\nt.pensize(3)\nt.forward(10)\n"
        "t.pencolor('blue')\nt.forward(10)\nturtle.colormode(255)\nt.pencolor(255, 128, 0)\nt.forward(5)\n"
    )
    assert [s.colour for s in d.strokes] == ["red", "blue", "#ff8000"]
    assert d.strokes[0].width == 3
    assert d.colours() == ["red", "blue", "#ff8000"]
    d2 = record_source("import turtle\nturtle.pencolor((1.0, 0.5, 0.0))\nturtle.forward(1)\n")
    assert d2.strokes[0].colour == "#ff8000"


def test_fill_dot_write_and_screen():
    d = record_source(
        "import turtle\ns = turtle.Screen()\ns.bgcolor('black')\ns.title('Stars')\n"
        "t = turtle.Turtle()\nt.fillcolor('yellow')\nt.begin_fill()\n"
        "for i in range(3):\n    t.forward(60)\n    t.left(120)\nt.end_fill()\n"
        "t.dot(8, 'white')\nt.write('hello', align='center')\ns.exitonclick()\n"
    )
    assert len(d.fills) == 1 and d.fills[0].colour == "yellow"
    assert same_polygon(d.fills[0].points, [(0, 0), (60, 0), (30, 60 * math.sqrt(3) / 2)])
    assert d.dots[0].colour == "white" and d.dots[0].size == 8
    assert d.texts[0].text == "hello" and d.texts[0].align == "center"
    assert d.screen.background == "black" and d.screen.window_title == "Stars"


def test_two_turtles_are_kept_apart():
    d = record_source(
        "import turtle\na = turtle.Turtle()\nb = turtle.Turtle()\nb.left(90)\na.forward(10)\nb.forward(10)\n"
    )
    assert [s.turtle for s in d.strokes] == [0, 1]
    assert close(d.strokes[1].points[-1], (0, 10))


def test_input_reads_the_given_text():
    d = record_source("import turtle\nn = int(input('Sides? '))\nfor i in range(n):\n"
                      "    turtle.forward(20)\n    turtle.left(360 / n)\n", stdin="5\n")
    assert len(d.strokes[0].points) == 6
    d2 = record_source("import turtle\nsize = turtle.numinput('Size', 'How big?')\nturtle.forward(size)\n",
                       stdin="42\n")
    assert close(d2.strokes[0].points[-1], (42, 0))


def test_endless_loop_is_stopped():
    with pytest.raises(TooManyMoves):
        record_source("import turtle\nwhile True:\n    turtle.forward(1)\n", max_moves=1000)


def test_events_are_recorded_not_waited_for():
    d = record_source(
        "import turtle\ns = turtle.Screen()\ndef up():\n    turtle.forward(10)\n"
        "s.onkey(up, 'Up')\ns.listen()\nturtle.mainloop()\n"
    )
    assert d.strokes == []
    assert "key:Up" in d.screen.handlers


def test_real_module_is_restored():
    import turtle as before
    record_source(SQUARE)
    import turtle as after
    assert after is before
    assert hasattr(after, "TurtleScreen")


def test_record_a_file_and_the_command_line(tmp_path):
    prog = tmp_path / "square.py"
    prog.write_text(SQUARE + "print('drawn')\n", encoding="utf-8")
    d = record(prog)
    assert d.printed == "drawn\n"
    out = tmp_path / "out" / "square.dat"
    d.write_dat(out)
    text = out.read_text(encoding="utf-8")
    assert text.splitlines()[0] == "# stroke 0 colour=black width=1"
    assert text.splitlines()[1:] == ["0 0", "100 0", "100 100", "0 100", "0 0"]
    out2 = tmp_path / "cli.dat"
    r = subprocess.run([sys.executable, "-m", "turtlerec", str(prog), str(out2)], capture_output=True,
                       text=True, cwd=HERE, env={"PYTHONPATH": str(HERE), "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("square.py: 1 strokes, 5 points")
    assert out2.read_text(encoding="utf-8") == text


def test_dat_blocks_and_fills(tmp_path):
    d = record_source("import turtle\nturtle.forward(1)\nturtle.penup()\nturtle.forward(1)\n"
                      "turtle.pendown()\nturtle.begin_fill()\nturtle.forward(1)\nturtle.left(90)\n"
                      "turtle.forward(1)\nturtle.end_fill()\n")
    blocks = d.dat().split("\n\n")
    assert len(blocks) == 2
    assert d.fills_dat().splitlines()[-1] == d.fills_dat().splitlines()[1]  # closed
    assert d.dat(colour="red") == ""


def test_fmt_simplify_and_same_polygon():
    assert fmt(-0.00001) == "0" and fmt(2.5) == "2.5" and fmt(100.0) == "100" and fmt(1 / 3) == "0.3333"
    pts = [(0, 0), (5, 0), (10, 0), (10, 0), (10, 10)]
    assert simplify(pts) == [(0, 0), (10, 0), (10, 10)]
    sq = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    assert same_polygon(sq, [(1, 1), (1, 0), (0, 0), (0, 1), (1, 1)])  # other start, other direction
    assert same_polygon([(0, 0.5), (0, 0), (1, 0), (1, 1), (0, 1), (0, 0.5)], sq)  # start mid-side
    assert not same_polygon(sq, [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])


def test_heading_and_position_match_the_real_navigator():
    d = record_source("import turtle\nt = turtle.Turtle()\nt.left(30)\nt.forward(10)\n"
                      "print(round(t.heading(), 6), t.pos())\nt.setheading(270)\nt.home()\n")
    t = d.turtles[0]
    assert t.heading() == 0
    assert close(t.pos(), (0, 0))
    assert "30.0" in d.printed


def test_package_names():
    assert "record" in turtlerec.__all__
