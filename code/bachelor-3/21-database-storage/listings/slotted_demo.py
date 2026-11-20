"""slotted_demo.py -- the town's people as records in one slotted page: insert, delete,
insert again, compact, and the header and slots after each step."""

import csv
from pathlib import Path

from slotted import SlottedPage

PEOPLE = Path(__file__).resolve().parents[4] / "data" / "town" / "people.csv"


def show(page, title):
    count, start = page.header()
    slots = " ".join(
        f"{i}:{o}+{n}" for i, (o, n) in enumerate(map(page.slot, range(count)))
    )
    print(
        f"{title}: {count} slots, records from byte {start}, free {page.free_space()}"
    )
    print(f"  slots (offset+length): {slots}")


rows = list(csv.DictReader(open(PEOPLE)))
page = SlottedPage()
for r in rows[:5]:
    page.insert(f"{r['person_id']},{r['first_name']},{r['last_name']}".encode())
show(page, "five records")
page.delete(1)
page.delete(3)
show(page, "slots 1 and 3 deleted")
rid = page.insert(b"121,Nora,Hillside")
show(page, f"one inserted in slot {rid}")
page.compact()
show(page, "compacted")
print("record 4 is still", page.get(4))
filled = SlottedPage()
n = sum(1 for r in rows if filled.insert(",".join(r.values()).encode()) is not None)
print(
    f"all {len(rows)} people offered to an empty page: {n} fit, "
    f"{filled.free_space()} bytes free"
)
