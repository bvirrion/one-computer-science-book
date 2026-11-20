"""exo_extra_fds.py: the dependencies A -> B between two single attributes that hold
in the town's 400 loan lines, but do not follow from the library's rules."""
import sqlite3
from pathlib import Path

import sqlrun
from fd import closure
from fd_demo import RULES, WIDE

conn = sqlite3.connect(":memory:")
sqlrun.run(conn, str(Path(__file__).with_name("wide_build.sql")), echo=False)
rows = conn.execute("SELECT * FROM wide").fetchall()  # the columns in WIDE's order
col = {a: i for i, a in enumerate(WIDE)}
for a in WIDE:
    seen = {}
    extra = [b for b in WIDE if b != a and b not in closure({a}, RULES)
             and all(seen.setdefault((b, r[col[a]]), r[col[b]]) == r[col[b]]
                     for r in rows)]
    if extra:
        print(f"{a:8} -> {', '.join(extra)}")
