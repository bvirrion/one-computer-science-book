"""Letter counts of the passage and of its shift-3 ciphertext, for the bar charts.

    python code/grade-9/06-first-cryptography/figures/letter_counts.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LISTINGS = HERE.parent / "listings"
sys.path.insert(0, str(LISTINGS))

from frequencies import letter_counts  # noqa: E402
from shift import ALPHABET, encrypt  # noqa: E402

passage = (LISTINGS / "passage.txt").read_text(encoding="utf-8")
plain = letter_counts(passage)
cipher = letter_counts(encrypt(passage, 3))
lines = ["letter plain cipher"]
for letter in ALPHABET:
    lines.append(f"{letter} {plain.get(letter, 0)} {cipher.get(letter, 0)}")
(HERE / "out").mkdir(exist_ok=True)
(HERE / "out" / "letters.dat").write_text("\n".join(lines) + "\n")
