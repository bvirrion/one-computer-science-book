"""index_timing.py: the loans of one member, found by scanning the table and then
through an index, on generated tables of growing size. Times on this machine."""
import random
import sqlite3
import time


def timed(conn, members, rng):
    """Mean time in microseconds of one query, over 200 random members."""
    ids = [rng.randrange(members) for _ in range(200)]
    t0 = time.perf_counter()
    for m in ids:
        conn.execute("SELECT count(*), max(out_day) FROM loans WHERE member_id = ?",
                     (m,)).fetchone()
    return (time.perf_counter() - t0) / len(ids) * 1e6


rng = random.Random(30)
print("     rows   scan (us)   index (us)   speed-up   index built in (ms)")
for n in [10_000, 100_000, 1_000_000]:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE loans (loan_id INTEGER PRIMARY KEY, member_id INTEGER,"
                 " book_id INTEGER, out_day INTEGER)")
    members = n // 20
    rows = ((i, rng.randrange(members), rng.randrange(5000), rng.randrange(365))
            for i in range(n))
    conn.executemany("INSERT INTO loans VALUES (?, ?, ?, ?)", rows)
    scan = timed(conn, members, rng)
    t0 = time.perf_counter()
    conn.execute("CREATE INDEX loans_member ON loans (member_id)")
    built = (time.perf_counter() - t0) * 1e3
    seek = timed(conn, members, rng)
    print(f"{n:9} {scan:11.0f} {seek:12.1f} {scan / seek:10.0f} {built:21.0f}")
    conn.close()
