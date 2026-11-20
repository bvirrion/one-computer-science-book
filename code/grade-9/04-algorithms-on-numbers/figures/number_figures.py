"""Data for the chapter's figures: the primes up to 100 and Euclid's longest runs.

    python code/grade-9/04-algorithms-on-numbers/figures/number_figures.py

out/primes.tex defines the list of primes the sieve grid colours, taken from the
sieve of the chapter; out/steps.dat gives, for each a up to 200, the largest number
of division steps of Euclid's algorithm over the pairs (a, b) with b < a.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))

from gcd import gcd  # noqa: E402
from sieve import sieve  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
primes = ",".join(str(p) for p in sieve(101))
(OUT / "primes.tex").write_text("\\def\\gnineprimes{" + primes + "}\n")
lines = ["a steps"]
for a in range(2, 201):
    lines.append(f"{a} {max(gcd(a, b)[1] for b in range(1, a))}")
(OUT / "steps.dat").write_text("\n".join(lines) + "\n")
