"""text_gen.py: the town archive, one line per loan and per weather reading, written
from the town's tables (no randomness: the same text on every run)."""
import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def archive():
    people = {p["person_id"]: f"{p['first_name']} {p['last_name']}"
              for p in rows("people")}
    member = {m["member_id"]: people[m["person_id"]] for m in rows("members")}
    title = {b["book_id"]: b["title"] for b in rows("books")}
    lines = []
    for loan in rows("loans"):
        who, what = member[loan["member_id"]], title[loan["book_id"]]
        lines.append(f"On {loan['out_date']}, {who} borrowed {what}.")
        if loan["return_date"]:
            lines.append(f"On {loan['return_date']}, {who} returned {what}.")
    for w in rows("weather"):
        if w["temp_c"]:
            lines.append(f"On {w['date']} at {w['station']}, {w['temp_c']} degrees and "
                         f"{w['rain_mm']} mm of rain.")
    return "\n".join(lines) + "\n"


def street_names():
    return [s["name"] for s in rows("streets")]
