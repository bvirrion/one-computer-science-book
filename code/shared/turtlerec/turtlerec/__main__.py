"""python -m turtlerec LISTING.py OUT.dat [--stdin FILE] [--fills FILLS.dat] [--colour NAME]

Runs an unchanged turtle program with the recording stand-in, writes its strokes as a .dat table and prints
a one-line summary.
"""
import argparse
from pathlib import Path

from turtlerec import record


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m turtlerec", description=__doc__.splitlines()[0])
    ap.add_argument("listing")
    ap.add_argument("out")
    ap.add_argument("--stdin", help="a file whose text the program's input() calls read")
    ap.add_argument("--fills", help="also write the filled shapes to this .dat file")
    ap.add_argument("--colour", help="write only the strokes of this pen colour")
    a = ap.parse_args(argv)
    stdin = Path(a.stdin).read_text(encoding="utf-8") if a.stdin else None
    d = record(a.listing, stdin=stdin)
    d.write_dat(a.out, colour=a.colour)
    if a.fills:
        d.write_fills_dat(a.fills)
    print(f"{Path(a.listing).name}: {d.summary()}")


if __name__ == "__main__":
    main()
