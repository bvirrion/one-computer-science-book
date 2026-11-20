"""ex5_learning.py -- a CDCL solver whose conflict analysis keeps only the
first-UIP literal and drops the literals of earlier levels. Find a formula it gets
wrong; fix it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from cdcl import CDCL  # noqa: E402


class Buggy(CDCL):
    def analyse(self, conflict):
        learned, _ = super().analyse(conflict)
        return learned[:1], 0  # BUG: the cut is not a cut; the clause is too strong


class Fixed(CDCL):
    pass  # the clause must keep the earlier-level literals, and backjump to the latest
