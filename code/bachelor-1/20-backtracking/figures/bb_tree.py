"""bb_tree.py: the nodes of branch and bound on the four-item knapsack of the figure,
in the order visited, with their value, room and bound."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from knapsack_bb import relaxation  # noqa: E402

THINGS = [(4, 40), (7, 42), (5, 25), (3, 12)]  # (weight, value), by decreasing v/w
CAPACITY = 10


def main():
    best = 0

    def visit(i, room, value, path):
        nonlocal best
        best = max(best, value)
        bound = value + relaxation(THINGS, i, room)
        if i == len(THINGS):
            print(f"{path or 'root':6} value {value:3} leaf, best {best}")
            return
        pruned = bound <= best
        print(f"{path or 'root':6} value {value:3} room {room:2} bound {bound:5.1f} "
              f"best {best:3}" + ("  pruned" if pruned else ""))
        if pruned:
            return
        w, v = THINGS[i]
        if w <= room:
            visit(i + 1, room - w, value + v, path + "1")
        visit(i + 1, room, value, path + "0")

    visit(0, CAPACITY, 0, "")


if __name__ == "__main__":
    main()
