"""timing_diagram.py: print the timing diagram of a program, one row per instruction."""
import sys

from pipeline import schedule, steps_of


def diagram(steps, forwarding=True, width=20):
    t = schedule(steps, forwarding)
    last = t.cycles
    rows = [" " * width + "".join(f"{c:>3}" for c in range(1, last + 1))]
    for s, f, d, x in zip(steps, t.fetch, t.decode, t.execute):
        cells = {f: "F", d: "D", x: "X", x + 1: "M", x + 2: "W"}  # IF, ID, EX, MEM, WB
        for c in range(f + 1, d):
            cells[c] = "."  # waiting in IF: the stage ahead is busy
        for c in range(d + 1, x):
            cells[c] = "*"  # stalled in ID: a bubble goes down the pipe
        line = "".join(f"{cells.get(c, ''):>3}" for c in range(1, last + 1))
        rows.append(f"{s.text:<{width}}{line}".rstrip())
    plural = "" if t.stalls == 1 else "s"
    summary = f"{len(steps)} instructions, {t.cycles} cycles"
    rows.append(f"{summary}, {t.stalls} stall cycle{plural}")
    return "\n".join(rows)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        steps = steps_of(f.read())
    forwarding = "--no-forwarding" not in sys.argv
    print(diagram(steps, forwarding))
