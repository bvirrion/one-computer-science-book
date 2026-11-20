"""overdue.py -- the library's late-loans report, run as three physical plans on
the town's tables, 10 tuples to a page, 5 buffer pages. Every intermediate result
is written out and read back; the page I/O is counted and compared with formulas."""

import math

import town
from exec import Disk, Relation, materialise, scan, select
from joins import block_nested_loop, build_index, hash_join, index_nested_loop
from selinger import best_plan

B = 5
T = {t: Relation(town.load(t)) for t in ("loans", "books", "members", "people")}
KEYS = [("book_id", "books"), ("member_id", "members"), ("person_id", "people")]


def late(t):
    return t["return_date"] is None or t["return_date"] > t["due_date"]


def plan_a(disk):  # as written: block nested loops, selection last
    cur = T["loans"]
    for col, table in KEYS:
        cur = materialise(block_nested_loop(cur, T[table], col, col, B, disk), disk)
    return list(select(late, scan(cur, disk)))  # the last join's result is read back


def plan_b(disk):  # selection pushed down, hash joins in the order Selinger picks
    loans = materialise(select(late, scan(T["loans"], disk)), disk)
    cur = materialise(
        hash_join(T["people"], T["members"], "person_id", "person_id", B, disk), disk
    )
    cur = materialise(hash_join(cur, loans, "member_id", "member_id", B, disk), disk)
    return hash_join(cur, T["books"], "book_id", "book_id", B, disk)


def plan_c(disk):  # selection pushed down, then index nested loops on the keys
    cur = materialise(select(late, scan(T["loans"], disk)), disk)
    for col, table in KEYS:
        rows = index_nested_loop(cur, T[table], col, col, INDEX[table], disk)
        if table != "people":
            cur = materialise(rows, disk)
    return rows


INDEX = {table: build_index(T[table], col) for col, table in KEYS}

if __name__ == "__main__":
    print("pages:", ", ".join(f"{t} {len(r)}" for t, r in T.items()) + f"; B = {B}")
    results = []
    for name, plan in (
        ("A  block nested loops, select last", plan_a),
        ("B  select first, hash joins (Selinger)", plan_b),
        ("C  select first, index nested loops", plan_c),
    ):
        disk = Disk()
        rows = plan(disk)
        results.append(sorted(r["loan_id"] for r in rows))
        print(
            f"{name:<38} {len(rows)} rows, {disk.reads:>5} reads, "
            f"{disk.writes:>4} writes, {disk.io():>5} page I/O"
        )
    print("same rows:", results[0] == results[1] == results[2])
    n_late = len(results[0])
    sizes = {"late_loans": n_late, "books": 80, "members": 60, "people": 120}
    preds = {
        frozenset({"late_loans", "books"}): ("book_id", 1 / 80),
        frozenset({"late_loans", "members"}): ("member_id", 1 / 60),
        frozenset({"members", "people"}): ("person_id", 1 / 120),
    }
    (cost, t, plan), costed = best_plan(sizes, preds, B)
    print(
        f"Selinger: {plan}\n  model cost {cost}, estimated {t:.0f} rows, "
        f"{costed} plans costed for {math.factorial(4)} orders"
    )
