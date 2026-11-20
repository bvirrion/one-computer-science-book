"""sqlite_header.py -- create a small SQLite database file with Python's sqlite3 and
decode the 100-byte header at the start of its first page, field by field, as the
file-format documentation lays it out (all integers big-endian)."""

import sqlite3
import struct
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "town.db"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT)")
    db.executemany(
        "INSERT INTO people (name) VALUES (?)", [(f"p{i}",) for i in range(2000)]
    )
    db.commit()
    db.close()
    raw = path.read_bytes()

header = raw[:100]
page_size = struct.unpack_from(">H", header, 16)[0]
fields = {
    "magic string": header[:16],
    "page size (bytes)": 65536 if page_size == 1 else page_size,
    "write / read format versions": (header[18], header[19]),
    "reserved bytes per page": header[20],
    "file change counter": struct.unpack_from(">I", header, 24)[0],
    "database size (pages)": struct.unpack_from(">I", header, 28)[0],
    "schema format number": struct.unpack_from(">I", header, 44)[0],
    "text encoding (1 = UTF-8)": struct.unpack_from(">I", header, 56)[0],
}
for name, value in fields.items():
    print(f"{name:<30} {value}")
print(f"file size {len(raw):,} bytes = {len(raw) // page_size} pages of {page_size}")
print("SQLite library version", sqlite3.sqlite_version)
