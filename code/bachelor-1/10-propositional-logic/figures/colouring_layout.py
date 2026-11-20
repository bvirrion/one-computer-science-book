"""Write colouring_graph.tex: the friendship graph, coloured by the SAT model."""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))

from colouring import COLOURS, colouring_cnf, friendships  # noqa: E402
from quine import quine  # noqa: E402

OUT = HERE / "colouring_graph.tex"
GROUPS = [(range(1, 15), (0.0, 0.0), 2.3), (range(15, 28), (7.2, 0.0), 2.1),
          (range(28, 40), (3.6, -4.6), 2.0)]
FILL = {"red": "red!45", "green": "green!45", "blue": "blue!30"}


def positions():
    pos = {}
    for people, (cx, cy), r in GROUPS:
        for k, p in enumerate(people):
            angle = math.pi / 2 - 2 * math.pi * k / len(people)
            x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
            pos[p] = (round(x, 3), round(y, 3))
    return pos


def lines():
    edges = friendships()
    people = sorted({p for edge in edges for p in edge})
    model = quine(colouring_cnf(people, edges, COLOURS), {"nodes": 0})
    colour = {p: next(c for c in COLOURS if f"{c}{p}" in model) for p in people}
    pos = positions()
    out = ["% written by figures/colouring_layout.py; do not edit"]
    for a, b in edges:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        out.append(f"\\draw[gray] ({xa},{ya}) -- ({xb},{yb});")
    for p in people:
        x, y = pos[p]
        style = "circle, draw, minimum size=5mm, inner sep=0pt, font=\\scriptsize"
        out.append(f"\\node[{style}, fill={FILL[colour[p]]}] at ({x},{y}) {{{p}}};")
    return out


if __name__ == "__main__":
    OUT.write_text("\n".join(lines()) + "\n")
