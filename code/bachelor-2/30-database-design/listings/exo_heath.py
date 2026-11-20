"""exo_heath.py: three splits of the wide table into two tables, tested by the chase."""
from fd import lossless
from fd_demo import RULES, WIDE

MEMBER = {"member", "first", "last", "street", "postcode"}
r = frozenset(WIDE)
for name, common in [("on member", {"member"}), ("on street", {"street"}),
                     ("on last name", {"last"})]:
    left, right = (r - MEMBER) | common, frozenset(MEMBER)  # common lies in both
    print(f"split {name:12}: lossless {lossless(r, [left, right], RULES)}")
