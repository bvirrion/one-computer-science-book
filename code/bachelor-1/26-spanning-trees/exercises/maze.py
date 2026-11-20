"""maze.py: a maze on a grid by Kruskal's algorithm on random weights: the walls taken
down are the edges of a spanning tree, so every cell is reachable by one way only."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from union_find import UnionFind  # noqa: E402


def maze(rows, cols, seed):
    rng = random.Random(seed)
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    walls = [((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)]
    walls += [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    rng.shuffle(walls)  # random order = random distinct weights
    uf, opened = UnionFind(cells), []
    for a, b in walls:
        if uf.union(a, b):
            opened.append((a, b))
    return opened


def draw(rows, cols, opened):
    open_set = set(opened)
    lines = ["+" + "--+" * cols]
    for r in range(rows):
        row, below = "|", "+"
        for c in range(cols):
            row += "  " + (" " if ((r, c), (r, c + 1)) in open_set else "|")
            below += ("  " if ((r, c), (r + 1, c)) in open_set else "--") + "+"
        lines += [row, below]
    return "\n".join(lines)


if __name__ == "__main__":
    print(draw(5, 12, maze(5, 12, seed=26)))
