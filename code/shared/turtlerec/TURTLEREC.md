FROZEN 2026-11-20 (Book 1)

# turtlerec: the recording turtle

The books print turtle programs exactly as a reader types them (`import turtle`, `forward`, `left`, …), but
the build machine has no display. `turtlerec` runs such a program **unchanged**, with a stand-in `turtle`
module that draws nothing and records every line, fill, dot and text, then writes the strokes as a `.dat`
table that a pgfplots figure draws. Book 1 (grade 6 onwards) uses it; Book 2 g12 may use it for recursive
drawings.

**Frozen:** figures depend on these coordinates. Wrap it in your chapter's `figures/` code; never edit this
package. Report a defect to the main session.

## Using it

From a chapter's `figures/` script or `tests/`:

```python
from turtlerec import record, same_polygon
d = record(LISTINGS / "square.py")              # runs it as __main__, from its own folder
d.write_dat(HERE / "out" / "square.dat")        # the figure's \addplot table
assert same_polygon(d.strokes[0].points, [(0, 0), (100, 0), (100, 100), (0, 100)])
```

or from the command line, with `code/shared/turtlerec` on `PYTHONPATH`:

```sh
PYTHONPATH=code/shared/turtlerec python -m turtlerec code/grade-6/03-for-loops-turtle/listings/square.py \
    out/square.dat [--stdin square.stdin] [--fills fills.dat] [--colour red]
```

`tools/test_code.sh` and `tools/capture_output.py` do not put `code/shared/turtlerec` on `PYTHONPATH`; a
chapter's `tests/conftest.py` (or its `figures/` script) adds it with one `sys.path.insert`. Turtle listings
are in their chapter's `listings/NORUN.txt`: no output file is captured for them, and the text says the
reader sees the drawing in a window.

## What it records

`record(path, stdin=None, max_moves=200000, quiet=True)` and `record_source(text, stdin=None, max_moves=…)`
return a `Drawing`:

| Field | Content |
|---|---|
| `strokes` | `Stroke(colour, width, points, turtle)`: a line drawn without lifting the pen or changing its colour or width; `points` are `(x, y)` floats, start included; never a one-point stroke |
| `fills` | `Fill(colour, points, turtle)`: the points visited between `begin_fill()` and `end_fill()` (open; `fills_dat()` closes them) |
| `dots` | `Dot(x, y, size, colour, turtle)`, with the real turtle's default size `pensize + max(pensize, 4)` |
| `texts` | `Text(x, y, text, align, font, turtle)` from `write` (`move=True` is refused: it needs a window to measure the text) |
| `turtles` | the turtle objects, in creation order (the anonymous turtle of module-level calls included); `heading()`, `pos()` work on them afterwards |
| `screen` | `background`, `window_title`, `size`, `handlers` (`"key:Up"`, `"keypress:space"`, `"click:1"`, `"turtle0:click:1"` → the function), `timers` |
| `moves`, `printed` | the number of moves; what the program printed (discarded from the terminal unless `quiet=False`) |

Helpers: `segments()`, `bbox()`, `colours()`, `dat(colour=None)`, `fills_dat()`, `write_dat(path,
colour=None)`, `write_fills_dat(path)`, `summary()`; module functions `simplify(points)` (drops repeated
points and the middle of straight runs), `same_polygon(a, b, tol=1e-6)` (same corners whatever the start and
direction, a straight run through the start ignored), `fmt(v)` (4 decimals, no trailing zeros, never `-0`).

`.dat` format: one block per stroke, a comment line `# stroke 3 colour=red width=2`, then `x y` lines; blocks
are separated by an empty line, which pgfplots reads as a jump (`empty line=jump`, its default for 2D plots).
Draw one colour per `\addplot` with `dat(colour=...)` / `write_dat(..., colour=...)`.

## Exactness

Movement is not reimplemented: `RecTurtle` inherits from the standard library's `turtle.TNavigator` and
`turtle.TPen`, the same classes every real `turtle.Turtle` inherits from, and only replaces the hooks that
would draw (`_goto`, `_newLine`, `_update`, colour lookup). So positions, headings and circles (`circle`'s
inscribed polygon with `1 + int(min(11 + |r|/6, 59) × extent/360)` steps) are the real turtle's, float for
float, on the Python that runs it (3.12 in `.venv`).

Colour names are kept as typed (no window to check them against); tuples become `#rrggbb` as in the real
turtle, under `colormode(1.0)` (default) or `colormode(255)`. Only the `standard` mode is recorded.

## What does not wait

`done`, `mainloop`, `exitonclick`, `bye`, `listen` return at once; event handlers (`onkey`, `onclick`,
`ontimer`) are stored in `screen.handlers` / `screen.timers`, never called (a test may call them).
`input()`, `textinput` and `numinput` read the `stdin` text given to `record`. An endless loop raises
`TooManyMoves` after `max_moves` moves. `undo` and shapes other than the name are not recorded. The real
`turtle` module is put back in `sys.modules` after each recording.

## Tests

`tests/test_turtlerec.py` (17 tests): corners of a square, module-level and `from turtle import *` calls,
strokes split by `penup` and colour changes, circles on the standard library's rule, regular polygons with
`steps`, fills, dots, text, the screen, two turtles, input, endless loops, events, the real module restored,
the command line and the `.dat` format.
