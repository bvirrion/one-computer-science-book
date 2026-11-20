"""Write figures/out/letters.dat: the letter counts of the passage of passage_stats.py.

    python code/grade-7/03-strings/figures/letter_counts.py
"""

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent


def passage():
    tree = ast.parse((HERE.parent / "listings" / "passage_stats.py").read_text())
    return tree.body[0].value.value


def main():
    text = passage().lower()
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    rows = [f"{c} {text.count(c)}" for c in "abcdefghijklmnopqrstuvwxyz"]
    (out / "letters.dat").write_text("letter count\n" + "\n".join(rows) + "\n")
    print("wrote", out / "letters.dat")


if __name__ == "__main__":
    main()
