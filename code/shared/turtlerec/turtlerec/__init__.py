"""turtlerec: run an unchanged turtle program without a window and record what it draws.

    from turtlerec import record
    drawing = record("listings/square.py")          # runs the file with a recording `turtle` module
    drawing.strokes[0].points                        # [(0.0, 0.0), (100.0, 0.0), ...]
    drawing.write_dat("figures/out/square.dat")      # "x y" lines, a blank line between strokes

The positions are computed by the standard library's own `turtle.TNavigator` (the class every real turtle
inherits its movement from), so the recorded coordinates are the ones the real turtle would reach, circles
included. Nothing is drawn and no window is opened. See TURTLEREC.md.
"""
from __future__ import annotations

import contextlib
import io
import math
import os
import runpy
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path

import turtle as _real

__all__ = [
    "Drawing", "Stroke", "Fill", "Dot", "Text", "TooManyMoves", "record", "record_source",
    "simplify", "same_polygon", "fmt",
]

MAX_MOVES = 200_000


class TooManyMoves(RuntimeError):
    """The program moved a turtle more than max_moves times (an endless loop, most likely)."""


@dataclass
class Stroke:
    """One line drawn without lifting the pen or changing its colour or width."""
    colour: str
    width: float
    points: list[tuple[float, float]] = field(default_factory=list)
    turtle: int = 0


@dataclass
class Fill:
    """A filled shape: the points visited between begin_fill() and end_fill()."""
    colour: str
    points: list[tuple[float, float]]
    turtle: int = 0


@dataclass
class Dot:
    x: float
    y: float
    size: float
    colour: str
    turtle: int = 0


@dataclass
class Text:
    x: float
    y: float
    text: str
    align: str
    font: tuple
    turtle: int = 0


def fmt(v: float) -> str:
    """A coordinate as printed in .dat files: 4 decimals, no trailing zeros, never -0."""
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


@dataclass
class Drawing:
    """Everything a program drew, in order."""
    strokes: list[Stroke] = field(default_factory=list)
    fills: list[Fill] = field(default_factory=list)
    dots: list[Dot] = field(default_factory=list)
    texts: list[Text] = field(default_factory=list)
    turtles: list = field(default_factory=list)      # the RecTurtle objects, in creation order
    screen: object = None                             # the RecScreen (background, title, handlers)
    moves: int = 0

    def segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        """Every drawn segment ((x1, y1), (x2, y2)), stroke by stroke."""
        out = []
        for s in self.strokes:
            out.extend(zip(s.points, s.points[1:]))
        return out

    def bbox(self) -> tuple[float, float, float, float]:
        """(xmin, ymin, xmax, ymax) of every stroke, fill and dot point."""
        pts = [p for s in self.strokes for p in s.points] + [p for f in self.fills for p in f.points]
        pts += [(d.x, d.y) for d in self.dots]
        if not pts:
            return (0.0, 0.0, 0.0, 0.0)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def colours(self) -> list[str]:
        """The pen colours used by strokes, in order of first use."""
        seen: list[str] = []
        for s in self.strokes:
            if s.colour not in seen:
                seen.append(s.colour)
        return seen

    def dat(self, colour: str | None = None) -> str:
        """The strokes as pgfplots-ready text: a comment per stroke, "x y" lines, a blank line between."""
        blocks = []
        for i, s in enumerate(self.strokes):
            if colour is not None and s.colour != colour:
                continue
            lines = [f"# stroke {i} colour={s.colour or 'none'} width={fmt(s.width)}"]
            lines += [f"{fmt(x)} {fmt(y)}" for x, y in s.points]
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks) + "\n" if blocks else ""

    def fills_dat(self) -> str:
        """The fills, closed (first point repeated), in the same format."""
        blocks = []
        for i, f in enumerate(self.fills):
            pts = f.points + f.points[:1]
            lines = [f"# fill {i} colour={f.colour or 'none'}"]
            lines += [f"{fmt(x)} {fmt(y)}" for x, y in pts]
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks) + "\n" if blocks else ""

    def write_dat(self, path, colour: str | None = None) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.dat(colour), encoding="utf-8")
        return p

    def write_fills_dat(self, path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.fills_dat(), encoding="utf-8")
        return p

    def summary(self) -> str:
        x0, y0, x1, y1 = self.bbox()
        npts = sum(len(s.points) for s in self.strokes)
        return (f"{len(self.strokes)} strokes, {npts} points, {len(self.fills)} fills, {len(self.dots)} dots, "
                f"{len(self.texts)} texts; box {fmt(x0)} {fmt(y0)} to {fmt(x1)} {fmt(y1)}")


def simplify(points, tol: float = 1e-6) -> list[tuple[float, float]]:
    """Drop repeated points and the middle points of straight runs (forward(10) five times is one side)."""
    out: list[tuple[float, float]] = []
    for p in points:
        if out and math.dist(out[-1], p) <= tol:
            continue
        if len(out) >= 2:
            (ax, ay), (bx, by) = out[-2], out[-1]
            cross = (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)
            dot = (bx - ax) * (p[0] - bx) + (by - ay) * (p[1] - by)
            if abs(cross) <= tol * max(1.0, math.dist(out[-2], p)) and dot >= 0:
                out[-1] = p
                continue
        out.append(p)
    return out


def same_polygon(a, b, tol: float = 1e-6) -> bool:
    """True if two closed paths have the same corners, whatever the starting corner and the direction."""
    def straight(a, b, c):
        cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        dot = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
        return abs(cross) <= tol * max(1.0, math.dist(a, c)) and dot >= 0

    def corners(pts):
        c = simplify(pts, tol)
        if len(c) > 1 and math.dist(c[0], c[-1]) <= tol:
            c = c[:-1]
        changed = True
        while changed and len(c) >= 3:  # also drop a straight run through the starting point
            changed = False
            for i in range(len(c)):
                if straight(c[i - 1], c[i], c[(i + 1) % len(c)]):
                    del c[i]
                    changed = True
                    break
        return c
    ca, cb = corners(list(a)), corners(list(b))
    if len(ca) != len(cb):
        return False
    n = len(ca)
    for seq in (cb, cb[::-1]):
        for k in range(n):
            if all(math.dist(ca[i], seq[(i + k) % n]) <= tol for i in range(n)):
                return True
    return False


# --------------------------------------------------------------------------- the recording turtle

def _colour(colormode, c) -> str:
    """The colour string the real turtle would store (names kept as typed, tuples as #rrggbb)."""
    if isinstance(c, str):
        return c
    try:
        r, g, b = c
    except (TypeError, ValueError):
        raise _real.TurtleGraphicsError(f"bad color arguments: {c}") from None
    if colormode == 1.0:
        r, g, b = (round(255.0 * x) for x in (r, g, b))
    if not all(0 <= v <= 255 for v in (r, g, b)):
        raise _real.TurtleGraphicsError(f"bad color sequence: {c}")
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


class RecScreen:
    """Stands for the turtle window. Methods that would wait for the user return at once."""

    def __init__(self, rec):
        self._rec = rec
        self.background = "white"
        self.window_title = ""
        self.size = None
        self.handlers: dict[str, object] = {}
        self.timers: list[tuple[object, int]] = []
        self.colormode_value = 1.0
        self.mode_value = "standard"

    # appearance
    def bgcolor(self, *args):
        if not args:
            return self.background
        self.background = _colour(self.colormode_value, args[0] if len(args) == 1 else args)

    def title(self, text):
        self.window_title = text

    def setup(self, width=None, height=None, startx=None, starty=None):
        self.size = (width, height)

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        if bg is not None:
            self.bgcolor(bg)
        return (canvwidth or 400, canvheight or 300)

    def colormode(self, cmode=None):
        if cmode is None:
            return self.colormode_value
        if cmode not in (1.0, 255):
            raise _real.TurtleGraphicsError(f"bad colormode: {cmode}")
        self.colormode_value = float(cmode) if cmode == 1.0 else 255

    def mode(self, mode=None):
        if mode is None:
            return self.mode_value
        if mode != "standard":
            raise NotImplementedError("turtlerec records the standard mode only")

    def turtles(self):
        return list(self._rec.turtles)

    # speed and refresh: nothing to animate
    def tracer(self, n=None, delay=None):
        return 1 if n is None else None

    def update(self):
        return None

    def delay(self, delay=None):
        return 0 if delay is None else None

    # waiting and events: recorded, never waited for
    def mainloop(self):
        return None

    done = mainloop

    def exitonclick(self):
        return None

    def bye(self):
        return None

    def listen(self, xdummy=None, ydummy=None):
        return None

    def onkey(self, fun, key=None):
        self.handlers[f"key:{key}"] = fun

    onkeyrelease = onkey

    def onkeypress(self, fun, key=None):
        self.handlers[f"keypress:{key}"] = fun

    def onclick(self, fun, btn=1, add=None):
        self.handlers[f"click:{btn}"] = fun

    onscreenclick = onclick

    def ontimer(self, fun, t=0):
        self.timers.append((fun, t))

    # questions to the user: read from standard input, as input() does
    def textinput(self, title, prompt):
        line = sys.stdin.readline()
        return None if line == "" else line.rstrip("\n")

    def numinput(self, title, prompt, default=None, minval=None, maxval=None):
        line = sys.stdin.readline()
        if line.strip() == "":
            return default
        return float(line)

    def clear(self):
        self._rec.strokes.clear()
        self._rec.fills.clear()
        self._rec.dots.clear()
        self._rec.texts.clear()

    clearscreen = clear

    def reset(self):
        for t in self._rec.turtles:
            t.reset()

    resetscreen = reset

    def window_width(self):
        return (self.size or (800, 600))[0]

    def window_height(self):
        return (self.size or (800, 600))[1]

    def register_shape(self, name, shape=None):
        return None

    addshape = register_shape

    def getshapes(self):
        return ["arrow", "blank", "circle", "classic", "square", "triangle", "turtle"]


class RecTurtle(_real.TPen, _real.TNavigator):
    """A turtle whose moves are computed by the real TNavigator and recorded instead of drawn."""

    def __init__(self, shape="classic", undobuffersize=0, visible=True, *, _rec=None):
        self._rec = _rec if _rec is not None else _current()
        self._id = len(self._rec.turtles)
        self._rec.turtles.append(self)
        self._shape = shape
        self._stroke = None
        self._fill_points = None
        _real.TNavigator.__init__(self, "standard")
        _real.TPen.__init__(self)
        self._shown = visible

    # hooks the real classes call ------------------------------------------------------------
    def _goto(self, end):
        self._rec.moves += 1
        if self._rec.moves > self._rec.max_moves:
            raise TooManyMoves(f"more than {self._rec.max_moves} moves: an endless loop?")
        start = (float(self._position[0]), float(self._position[1]))
        stop = (float(end[0]), float(end[1]))
        if self._drawing:
            if self._stroke is None:
                self._stroke = Stroke(self._pencolor, self._pensize, [start], self._id)
                self._rec.strokes.append(self._stroke)
            self._stroke.points.append(stop)
        if self._fill_points is not None:
            self._fill_points.append(stop)
        self._position = end

    def _newLine(self, usePos=True):
        self._stroke = None

    def _update(self):
        return None

    def _colorstr(self, color):
        if len(color) == 1:  # as turtle.TurtleScreen._colorstr: a 1-tuple, or a 1-letter name
            color = color[0]
        return _colour(self._rec.screen.colormode_value, color)

    def _color(self, cstr):
        return cstr

    def _tracer(self, a=None, b=None):
        return 1 if a is None else None

    def _delay(self, n=None):
        return 0 if n is None else None

    # what RawTurtle adds on top of TPen and TNavigator -------------------------------------
    def reset(self):
        _real.TNavigator.reset(self)
        _real.TPen._reset(self)
        self._stroke = None
        self._fill_points = None

    def teleport(self, x=None, y=None, *, fill_gap=False):
        self._stroke = None
        new = _real.Vec2D(self._position[0] if x is None else x, self._position[1] if y is None else y)
        if self._fill_points is not None and fill_gap:
            self._fill_points.append((float(new[0]), float(new[1])))
        self._position = new

    def begin_fill(self):
        self._fill_points = [(float(self._position[0]), float(self._position[1]))]

    def end_fill(self):
        if self._fill_points is not None and len(self._fill_points) > 2:
            self._rec.fills.append(Fill(self._fillcolor, self._fill_points, self._id))
        self._fill_points = None

    def filling(self):
        return self._fill_points is not None

    def dot(self, size=None, *color):
        if not color:
            if isinstance(size, (str, tuple)):
                c, size = self._colorstr((size,)), self._pensize + max(self._pensize, 4)
            else:
                c = self._pencolor
                size = size or self._pensize + max(self._pensize, 4)
        else:
            size = self._pensize + max(self._pensize, 4) if size is None else size
            c = self._colorstr(color)
        self._rec.dots.append(Dot(float(self._position[0]), float(self._position[1]), size, c, self._id))

    def write(self, arg, move=False, align="left", font=("Arial", 8, "normal")):
        x, y = float(self._position[0]), float(self._position[1])
        self._rec.texts.append(Text(x, y, str(arg), align, tuple(font), self._id))
        if move:  # the real turtle moves by the text's width, which needs a window: not recorded
            raise NotImplementedError("write(..., move=True) needs a real window")

    def stamp(self):
        return len(self._rec.dots)

    def clearstamp(self, stampid):
        return None

    def clearstamps(self, n=None):
        return None

    def clear(self):
        self._rec.strokes[:] = [s for s in self._rec.strokes if s.turtle != self._id]
        self._rec.fills[:] = [f for f in self._rec.fills if f.turtle != self._id]
        self._rec.dots[:] = [d for d in self._rec.dots if d.turtle != self._id]
        self._rec.texts[:] = [t for t in self._rec.texts if t.turtle != self._id]
        self._stroke = None

    def shape(self, name=None):
        if name is None:
            return self._shape
        self._shape = name

    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        return None

    turtlesize = shapesize

    def getscreen(self):
        return self._rec.screen

    def getturtle(self):
        return self

    getpen = getturtle

    def setundobuffer(self, size):
        return None

    def undo(self):
        raise NotImplementedError("turtlerec does not record undo")

    def onclick(self, fun, btn=1, add=None):
        self._rec.screen.handlers[f"turtle{self._id}:click:{btn}"] = fun

    onrelease = onclick
    ondrag = onclick

    def clone(self):
        t = RecTurtle(self._shape, _rec=self._rec)
        t._position, t._orient = self._position, self._orient
        t.pen(self.pen())
        return t


# --------------------------------------------------------------------------- the stand-in module

class _Recorder(Drawing):
    def __init__(self, max_moves):
        super().__init__()
        self.max_moves = max_moves
        self.screen = RecScreen(self)
        self.anonymous = None


_ACTIVE: list[_Recorder] = []


def _current() -> _Recorder:
    if not _ACTIVE:
        raise RuntimeError("turtlerec: no recording in progress")
    return _ACTIVE[-1]


_TURTLE_METHODS = [
    "back", "backward", "begin_fill", "bk", "circle", "clear", "clearstamp", "clearstamps", "clone", "color",
    "degrees", "distance", "dot", "down", "end_fill", "fd", "fillcolor", "filling", "forward", "getpen",
    "getscreen", "getturtle", "goto", "heading", "hideturtle", "home", "ht", "isdown", "isvisible", "left",
    "lt", "onclick", "ondrag", "onrelease", "pd", "pen", "pencolor", "pendown", "pensize", "penup", "pos",
    "position", "pu", "radians", "reset", "right", "rt", "seth", "setheading", "setpos", "setposition",
    "settiltangle", "setundobuffer", "setx", "sety", "shape", "shapesize", "showturtle", "speed", "st",
    "stamp", "teleport", "towards", "turtlesize", "undo", "up", "width", "write", "xcor", "ycor",
]
_SCREEN_METHODS = [
    "addshape", "bgcolor", "bye", "clearscreen", "colormode", "delay", "done", "exitonclick", "getshapes",
    "listen", "mainloop", "mode", "numinput", "onkey", "onkeypress", "onkeyrelease", "onscreenclick",
    "ontimer", "register_shape", "resetscreen", "screensize", "setup", "textinput", "title", "tracer",
    "turtles", "update", "window_height", "window_width",
]


def _anonymous() -> RecTurtle:
    rec = _current()
    if rec.anonymous is None:
        rec.anonymous = RecTurtle(_rec=rec)
    return rec.anonymous


def _module() -> types.ModuleType:
    m = types.ModuleType("turtle", "turtlerec's recording stand-in for the turtle module")

    def make_t(name):
        def f(*args, **kwargs):
            return getattr(_anonymous(), name)(*args, **kwargs)
        f.__name__ = name
        return f

    def make_s(name):
        def f(*args, **kwargs):
            return getattr(_current().screen, name)(*args, **kwargs)
        f.__name__ = name
        return f

    for n in _TURTLE_METHODS:
        if hasattr(RecTurtle, n):
            setattr(m, n, make_t(n))
    for n in _SCREEN_METHODS:
        setattr(m, n, make_s(n))
    m.Turtle = m.RawTurtle = m.Pen = m.RawPen = RecTurtle
    m.Screen = lambda: _current().screen
    m.getscreen = m.Screen
    m.Vec2D = _real.Vec2D
    m.TurtleGraphicsError = _real.TurtleGraphicsError
    m.Terminator = _real.Terminator
    m.__all__ = sorted(n for n in vars(m) if not n.startswith("_"))
    return m


@contextlib.contextmanager
def _recording(max_moves, stdin_text):
    rec = _Recorder(max_moves)
    _ACTIVE.append(rec)
    saved_mod = sys.modules.get("turtle")
    saved_stdin = sys.stdin
    sys.modules["turtle"] = _module()
    if stdin_text is not None:
        sys.stdin = io.StringIO(stdin_text)
    try:
        yield rec
    finally:
        sys.stdin = saved_stdin
        if saved_mod is None:
            sys.modules.pop("turtle", None)
        else:
            sys.modules["turtle"] = saved_mod
        _ACTIVE.pop()


def _finish(rec: _Recorder) -> Drawing:
    rec.strokes[:] = [s for s in rec.strokes if len(s.points) > 1]  # never a one-point stroke
    return Drawing(rec.strokes, rec.fills, rec.dots, rec.texts, rec.turtles, rec.screen, rec.moves)


def record(path, stdin: str | None = None, max_moves: int = MAX_MOVES, quiet: bool = True) -> Drawing:
    """Run the turtle program at `path` (as __main__, from its own folder) and return what it drew.

    `stdin` is the text its input() calls read. What the program prints is discarded unless quiet=False.
    """
    path = Path(path).resolve()
    old_cwd, old_argv, old_path0 = os.getcwd(), sys.argv, list(sys.path)
    out = io.StringIO()
    with _recording(max_moves, stdin) as rec:
        try:
            os.chdir(path.parent)
            sys.argv = [str(path)]
            sys.path.insert(0, str(path.parent))
            with contextlib.redirect_stdout(out) if quiet else contextlib.nullcontext():
                runpy.run_path(str(path), run_name="__main__")
        finally:
            os.chdir(old_cwd)
            sys.argv = old_argv
            sys.path[:] = old_path0
    d = _finish(rec)
    d.printed = out.getvalue()
    return d


def record_source(source: str, stdin: str | None = None, max_moves: int = MAX_MOVES) -> Drawing:
    """Run turtle code given as a string (for tests) and return what it drew. Its prints are discarded."""
    out = io.StringIO()
    with _recording(max_moves, stdin) as rec, contextlib.redirect_stdout(out):
        exec(compile(source, "<turtle program>", "exec"), {"__name__": "__main__"})
    d = _finish(rec)
    d.printed = out.getvalue()
    return d
