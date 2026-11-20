"""exo_synthesis.py: 3NF synthesis for the reading-room bookings."""
from fd import fds, is_3nf, lossless, minimal_cover, preserves, synthesis_3nf

R = frozenset(["seat", "day", "slot", "member", "desk", "name"])
DEPS = fds("seat day slot -> member desk; member day slot -> seat; seat -> desk;"
           " member -> name")
print("minimal cover:", "; ".join(f"{' '.join(sorted(a))} -> {' '.join(b)}"
                                  for a, b in minimal_cover(DEPS)))
parts = synthesis_3nf(R, DEPS)
for p in parts:
    print("table", sorted(p), "| 3NF:", is_3nf(p, DEPS))
print("lossless:", lossless(R, parts, DEPS), "| preserving:", preserves(parts, DEPS))
