"""Write town_astar_fig.tex: the town map with the places expanded by Dijkstra and by
A* from the Station to the Old Mill, and the route, as TikZ commands."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))

from state_space import astar  # noqa: E402
from town_map import ROADS, XY, straight  # noqa: E402

S, T = 2, 14
FIG = HERE / "town_astar_fig.tex"


def main():
    dij, ast = [], []
    astar(S, lambda x: x == T, lambda x: ROADS.get(x, []), order=dij)
    path, _, _ = astar(S, lambda x: x == T, lambda x: ROADS.get(x, []),
                       lambda x: straight(x, T), order=ast)
    on_path = set(zip(path, path[1:])) | set(zip(path[1:], path))
    out = []
    for u in sorted(ROADS):
        for v, _ in ROADS[u]:
            if u < v or u not in [w for w, _ in ROADS.get(v, [])]:
                style = "route" if (u, v) in on_path else "road"
                out.append(f"\\draw[{style}] (p{u}) -- (p{v});")
    nodes = []
    for p, (x, y) in sorted(XY.items()):
        kind = "astar" if p in ast else "dijkstra" if p in dij else "other"
        at = f"({x / 1000:.3f}, {y / 1000:.3f})"
        nodes.append(f"\\node[{kind}] (p{p}) at {at} {{{p}}};")
    head = ["% written by town_fig.py from the town map; do not edit"]
    FIG.write_text("\n".join(head + nodes + out) + "\n")
    return dij, ast


if __name__ == "__main__":
    main()
