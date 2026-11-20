"""Exercise: the members with more than three late returns, in relational algebra
(with the grouping operator gamma), compared with the SQL answer."""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
import town  # noqa: E402
from algebra import group, project, select, table  # noqa: E402


def late_members():
    loans = table("loans")
    late = select(loans, lambda t: t["return_date"] is not None
                  and t["return_date"] > t["due_date"])
    counts = group(late, ("member_id",), "late", len, "loan_id")
    return project(select(counts, lambda t: t["late"] > 3), ("member_id", "late"))


def by_sql():
    conn = sqlite3.connect(":memory:")
    town.to_sqlite(conn)
    text = (Path(__file__).with_suffix(".sql")).read_text()
    query = text.split("\n", 2)[2]  # skip the two comment lines
    return {tuple(r) for r in conn.execute(query)}


if __name__ == "__main__":
    print(sorted(late_members().rows), set(late_members().rows) == by_sql())
