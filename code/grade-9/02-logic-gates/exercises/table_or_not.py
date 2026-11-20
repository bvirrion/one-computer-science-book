from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from gates import AND, NOT, OR  # noqa: E402

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            print(a, b, c, "|", AND(OR(a, b), NOT(c)))
