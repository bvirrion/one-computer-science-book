"""Write friends_graph.tex: TikZ commands for the friendship graph of people 1-40."""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "friends_graph.tex"
GROUPS = [(range(1, 15), (0.0, 0.0), 2.3), (range(15, 28), (7.2, 0.0), 2.1),
          (range(28, 40), (3.6, -4.6), 2.0)]
BRIDGES = {(1, 28), (5, 37), (12, 20), (25, 37)}  # edges between the three groups


def positions():
    pos = {}
    for people, (cx, cy), r in GROUPS:
        n = len(people)
        for k, p in enumerate(people):
            angle = math.pi / 2 - 2 * math.pi * k / n
            x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
            pos[p] = (round(x, 3), round(y, 3))
    pos[40] = (8.6, -4.6)
    return pos


def edges():
    with open(HERE.parent / "listings" / "friendships.csv", newline="") as f:
        return [(int(r["person_a"]), int(r["person_b"])) for r in csv.DictReader(f)]


def main():
    pos = positions()
    lines = ["% written by figures/friends_layout.py; do not edit"]
    for a, b in edges():
        style = "gedge, omProp" if (a, b) in BRIDGES else "gedge"
        (xa, ya), (xb, yb) = pos[a], pos[b]
        lines.append(f"\\draw[{style}] ({xa},{ya}) -- ({xb},{yb});")
    for p, (x, y) in sorted(pos.items()):
        fill = "omDef!25" if p in (1, 28) else "white"
        node = f"gnode, minimum size=5mm, font=\\scriptsize, fill={fill}"
        lines.append(f"\\node[{node}] at ({x},{y}) {{{p}}};")
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
