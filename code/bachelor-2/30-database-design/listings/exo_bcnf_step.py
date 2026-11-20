"""exo_bcnf_step.py: one BCNF step on the wide table, splitting off a single
attribute of the violating dependency's right side, then the whole closure."""
from fd import bcnf_violation, closure
from fd_demo import RULES, WIDE, show

r = frozenset(WIDE)
for ys in [frozenset({"title"}), closure({"book"}, RULES) - {"book"}]:
    left, rest = frozenset({"book"}) | ys, r - ys
    print("split off", show(left))
    for part in (left, rest):
        v = bcnf_violation(part, RULES)
        print("   ", len(part), "attributes; still violated by",
              "nothing" if v is None else f"{show(v[0])} -> {show(v[1])}")
