"""redesign.py: the library's spreadsheet redesigned. The redundancy of the wide
table, its violations of BCNF, the four tables, and a member's move in each design."""
import sqlite3
from pathlib import Path

import sqlrun
from fd import bcnf, bcnf_violation, closure, lossless, minimal_cover, preserves
from fd_demo import RULES, WIDE, show

conn = sqlite3.connect(":memory:")
sqlrun.run(conn, str(Path(__file__).with_name("wide_build.sql")), echo=False)

# Part I: each fact is stored once per loan line.
for det, column in [("book", "book_id"), ("member", "member_id"), ("street", "street")]:
    sql = f"SELECT count(*), count(DISTINCT {column}) FROM wide"
    lines, values = conn.execute(sql).fetchone()
    print(f"facts of a {det:6}: {values:3} distinct, stored on {lines} lines,"
          f" {lines - values} copies too many")

# Part II: the left sides of the minimal cover that are not keys of the wide table.
bad = sorted({left for left, _ in minimal_cover(RULES)
              if closure(left, RULES) != frozenset(WIDE)}, key=sorted)
print("dependencies violating BCNF, by left side:", ", ".join(show(b) for b in bad))

# Part III: the BCNF tables; each checked, and the decomposition as a whole.
parts = bcnf(WIDE, RULES)
print(len(parts), "tables, violations left:",
      sum(bcnf_violation(p, RULES) is not None for p in parts),
      "| lossless:", lossless(WIDE, parts, RULES),
      "| preserving:", preserves(parts, RULES))

# Part IV: member 55 moves; one UPDATE in each design.
conn.execute("CREATE TABLE d_members AS SELECT DISTINCT member_id, first_name,"
             " last_name, street FROM wide")
wide = conn.execute("UPDATE wide SET street = 'Garden Lane', postcode = 'B-110'"
                    " WHERE member_id = 55").rowcount
one = conn.execute("UPDATE d_members SET street = 'Garden Lane'"
                   " WHERE member_id = 55").rowcount
print(f"the move: {wide} lines changed in the wide table, {one} in the members table")
