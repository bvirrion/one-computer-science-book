"""Exercise: a Mealy detector of 0110, overlaps allowed, tested on every word of up
to 12 bits against the plain definition."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from lock import detector  # noqa: E402
from seq import all_words  # noqa: E402


def check(longest=12):
    m = detector([0, 1, 1, 0])
    for w in all_words((0, 1), longest):
        want = [int(w[i - 3:i + 1] == (0, 1, 1, 0)) if i >= 3 else 0
                for i in range(len(w))]
        if m.run(w) != want:
            return False
    return True


if __name__ == "__main__":
    m = detector([0, 1, 1, 0])
    for (state, a), (nxt, out) in sorted(m.delta.items()):
        p, r = "".join(map(str, state)) or "e", "".join(map(str, nxt)) or "e"
        print(f"{p:>3} --{a}/{out}--> {r}")
    print("correct on every word of up to 12 bits:", check())
