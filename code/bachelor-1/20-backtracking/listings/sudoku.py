"""sudoku.py: a sudoku solved by backtracking on the most constrained empty cell."""

from pathlib import Path

DIGITS = set("123456789")


def read_grid(path):
    """81 characters, digits and '.', read row by row (other characters ignored)."""
    cells = [ch for ch in Path(path).read_text() if ch in DIGITS or ch == "."]
    assert len(cells) == 81
    return cells


def candidates(g, i):
    """The digits that cell i can take: none of its row, column or 3 x 3 box."""
    r, c = divmod(i, 9)
    br, bc = 3 * (r // 3), 3 * (c // 3)
    seen = {g[9 * r + k] for k in range(9)} | {g[9 * k + c] for k in range(9)}
    seen |= {g[9 * (br + a) + bc + b] for a in range(3) for b in range(3)}
    return DIGITS - seen


def solve(g, stats, first_empty=False):
    """Fill g in place; True if solved. stats["nodes"] counts the calls."""
    stats["nodes"] += 1
    empty = [i for i in range(81) if g[i] == "."]
    if not empty:
        return True
    if first_empty:
        i = empty[0]
    else:  # the empty cell with the fewest candidates
        i = min(empty, key=lambda j: len(candidates(g, j)))
    for d in sorted(candidates(g, i)):  # no candidate: a dead end, return False
        g[i] = d
        if solve(g, stats, first_empty):
            return True
    g[i] = "."
    return False


def show(g):
    for r in range(9):
        row = "".join(g[9 * r:9 * r + 9])
        print(" ".join([row[0:3], row[3:6], row[6:9]]))


def main():
    for rule in ("first empty cell", "most constrained cell"):
        g = read_grid(Path(__file__).with_name("grid.txt"))
        stats = {"nodes": 0}
        solved = solve(g, stats, first_empty=rule == "first empty cell")
        print(f"{rule}: solved {solved}, {stats['nodes']} nodes")
    show(g)


if __name__ == "__main__":
    main()
