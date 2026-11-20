"""cook_levin.py -- the proof of the Cook-Levin theorem run on a small machine: the
tableau of an accepting run of a nondeterministic machine, written as a CNF formula
whose satisfying assignments are exactly its accepting tableaux, then solved."""
import itertools

from dpll import dpll

TAPE, STATES = "01_", ("q0", "q1", "qa")
DELTA = {  # nondeterministic: on a 1, q0 may stay or guess "the next one is the pair"
    ("q0", "0"): [("q0", "0", "R")],
    ("q0", "1"): [("q0", "1", "R"), ("q1", "1", "R")],
    ("q1", "1"): [("qa", "1", "R")],
}
SYMBOLS = ["#", *TAPE, *STATES]


def successors(row):
    """The rows one step after row, a tuple '#', cells and one state, '#'."""
    h = next(i for i, s in enumerate(row) if s in STATES)
    if row[h] == "qa":
        return [row]  # an accepted run stays as it is
    out = []
    for q, w, move in DELTA.get((row[h], row[h + 1]), []):
        if move == "R" and row[h + 2] != "#":  # state moves right, past the written w
            out.append(row[:h] + (w, q) + row[h + 2:])
    return out


def legal_windows(width):
    """Every 2 x 3 window that occurs in some row and its successor."""
    windows = set()
    for h in range(1, width - 2):
        for q in STATES:
            for cells in itertools.product(TAPE, repeat=width - 3):
                row = ("#", *cells[:h - 1], q, *cells[h - 1:], "#")
                for nxt in successors(row):
                    windows |= {(row[j:j + 3], nxt[j:j + 3]) for j in range(width - 2)}
    return windows


def formula(word, steps):
    width = max(len(word), steps + 1) + 3  # room for the input and for the head
    num = {}

    def x(i, j, s):  # variable "cell j of row i holds symbol s"
        return num.setdefault((i, j, s), len(num) + 1)
    clauses = []
    for i, j in itertools.product(range(steps + 1), range(width)):
        clauses.append([x(i, j, s) for s in SYMBOLS])  # at least one symbol
        clauses += [[-x(i, j, s), -x(i, j, t)]  # at most one
                    for s, t in itertools.combinations(SYMBOLS, 2)]
    start = ("#", "q0", *word, *"_" * (width - len(word) - 3), "#")
    clauses += [[x(0, j, s)] for j, s in enumerate(start)]
    clauses.append([x(i, j, "qa") for i in range(steps + 1) for j in range(width)])
    windows = legal_windows(width)
    for i, j in itertools.product(range(steps), range(width - 2)):
        choice = []
        for top, bottom in windows:  # y means "this legal window is here"
            y = num.setdefault(("w", i, j, top, bottom), len(num) + 1)
            choice.append(y)
            clauses += [[-y, x(i, j + d, top[d])] for d in range(3)]
            clauses += [[-y, x(i + 1, j + d, bottom[d])] for d in range(3)]
        clauses.append(choice)
    return clauses, num, width, len(windows)


if __name__ == "__main__":
    word, steps = "011", 3
    clauses, num, width, legal = formula(word, steps)
    cells = sum(1 for k in num if k[0] != "w")
    print(f"input {word}, {steps} steps: tableau {steps + 1} x {width}, "
          f"{legal} legal windows")
    print(f"{len(num):,} variables ({cells} for cells), {len(clauses):,} clauses")
    solution = dpll(clauses)
    for i in range(steps + 1):
        row = [s for j in range(width) for s in SYMBOLS if solution[num[(i, j, s)]]]
        print(" ".join(f"{s:<2}" for s in row))
