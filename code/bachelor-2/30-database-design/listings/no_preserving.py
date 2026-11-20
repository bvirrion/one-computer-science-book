"""no_preserving.py: an address table where BCNF loses a dependency and 3NF keeps it.
A street and a town determine the postcode; a postcode lies in one town."""
from fd import bcnf, fds, is_3nf, keys, lossless, preserves, synthesis_3nf

R = frozenset(["street", "town", "postcode"])
DEPS = fds("street town -> postcode; postcode -> town")


def show(xs):
    return "{" + ", ".join(sorted(xs)) + "}"


print("keys:", " ".join(show(k) for k in keys(R, DEPS)), "| in 3NF:", is_3nf(R, DEPS))
for name, parts in [("BCNF", bcnf(R, DEPS)), ("3NF synthesis", synthesis_3nf(R, DEPS))]:
    print(f"{name:13}:", " ".join(show(p) for p in parts),
          f"| lossless {lossless(R, parts, DEPS)}, preserving {preserves(parts, DEPS)}")
