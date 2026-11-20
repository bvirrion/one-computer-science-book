"""town.py: the town's people and friendships, read from the shared tables."""
import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def people():
    """(last name, first name, id) for each person: distinct, comparable keys."""
    return [(p["last_name"], p["first_name"], int(p["person_id"]))
            for p in rows("people")]


def friendships():
    return [(int(r["person_a"]), int(r["person_b"])) for r in rows("friendships")]
