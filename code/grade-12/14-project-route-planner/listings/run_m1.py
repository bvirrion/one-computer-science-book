import sqlite3

from db import build

conn = build()
for table in ["place", "road"]:
    print(table, conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], "rows")
print("one-way:", conn.execute("SELECT road_id, from_place, to_place FROM road"
                               " WHERE one_way = 1").fetchall())
print("speeds:", conn.execute("SELECT speed_kmh, COUNT(*) FROM road"
                              " GROUP BY speed_kmh").fetchall())
TRIES = [("a road to place 99", "INSERT INTO road VALUES (54, 1, 99, 500, 50, 0)"),
         ("a negative length", "INSERT INTO road VALUES (54, 1, 2, -5, 50, 0)"),
         ("a second Station", "INSERT INTO place VALUES (31, 'Station', 'x')")]
for what, bad in TRIES:
    try:
        conn.execute(bad)
    except sqlite3.IntegrityError as e:
        print(f"refused, {what}: {e}")
