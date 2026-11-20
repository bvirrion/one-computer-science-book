"""Exercise 15: export members with their loans to JSON, and read them back."""
import json


def members_with_loans(members, loans):
    by_member = {}
    for loan in loans:
        entry = {"book": loan["book_id"], "out": loan["out_date"],
                 "back": loan["return_date"]}
        by_member.setdefault(loan["member_id"], []).append(entry)
    return [{"member_id": m["member_id"], "loans": by_member.get(m["member_id"], [])}
            for m in members]


def round_trip(data):
    return json.loads(json.dumps(data)) == data
