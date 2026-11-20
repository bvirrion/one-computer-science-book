"""Write per_letter.dat: comparisons per text letter against the pattern's length."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from horspool import horspool  # noqa: E402
from naive import search_naive  # noqa: E402

rng = random.Random(4)
n = 50_000
texts = {a: "".join(rng.choice(a) for _ in range(n))
         for a in ["abcdefghijklmnopqrstuvwxyz", "ACGT"]}
with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("m naive26 hors26 naive4 hors4\n")
    for m in range(2, 33, 2):
        row = [str(m)]
        for text in texts.values():
            starts = [rng.randrange(n - m) for _ in range(5)]
            naive = sum(search_naive(text, text[s:s + m])[1] for s in starts) / 5 / n
            hors = sum(horspool(text, text[s:s + m])[1] for s in starts) / 5 / n
            row += [f"{naive:.3f}", f"{hors:.3f}"]
        out.write(" ".join(row) + "\n")
