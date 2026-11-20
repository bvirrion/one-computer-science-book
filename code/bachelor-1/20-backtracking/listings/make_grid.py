"""make_grid.py: a sudoku with a unique solution and few clues, made reproducibly:
fill a grid at random, then remove clues while the solution stays unique."""

import random
from pathlib import Path

from sudoku import candidates


def count_solutions(g, limit=2):
    empty = [i for i in range(81) if g[i] == "."]
    if not empty:
        return 1
    i = min(empty, key=lambda j: len(candidates(g, j)))
    total = 0
    for d in candidates(g, i):
        g[i] = d
        total += count_solutions(g, limit - total)
        if total >= limit:
            break
    g[i] = "."
    return total


def fill(g, rng):
    empty = [i for i in range(81) if g[i] == "."]
    if not empty:
        return True
    i = min(empty, key=lambda j: len(candidates(g, j)))
    digits = sorted(candidates(g, i))
    rng.shuffle(digits)
    for d in digits:
        g[i] = d
        if fill(g, rng):
            return True
    g[i] = "."
    return False


def main():
    rng = random.Random(20)
    g = ["."] * 81
    fill(g, rng)
    order = list(range(81))
    rng.shuffle(order)
    for i in order:  # remove a clue unless the puzzle would get a second solution
        keep, g[i] = g[i], "."
        if count_solutions(list(g)) != 1:
            g[i] = keep
    text = "\n".join("".join(g[9 * r:9 * r + 9]) for r in range(9)) + "\n"
    Path(__file__).with_name("grid.txt").write_text(text)
    print(f"{81 - g.count('.')} clues")
    print(text, end="")


if __name__ == "__main__":
    main()
