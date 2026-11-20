"""loans_by_member.py: the loans sorted by member, and by date within a member, with a
stable sort applied twice: first by the secondary key, then by the primary key."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def loans():
    with open(TOWN / "loans.csv", newline="") as f:
        return [(int(r["member_id"]), r["out_date"], int(r["loan_id"]))
                for r in csv.DictReader(f)]


def by_member_then_date(rows):
    rows = sorted(rows, key=lambda r: r[1])  # secondary key first
    return sorted(rows, key=lambda r: r[0])  # stable: dates keep their order
