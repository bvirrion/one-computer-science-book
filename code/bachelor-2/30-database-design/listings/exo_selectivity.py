"""exo_selectivity.py: a range query answered through an index and by a full scan, as
the fraction of rows it selects grows. Times on this machine."""
import random
import sqlite3
import time

rng = random.Random(12)
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE loans (loan_id INTEGER PRIMARY KEY, out_day INTEGER,"
             " pages INTEGER)")
n = 400_000
conn.executemany("INSERT INTO loans VALUES (?, ?, ?)",
                 ((i, rng.randrange(100_000), rng.randrange(900)) for i in range(n)))
conn.execute("CREATE INDEX loans_day ON loans (out_day)")


def best_of_3(sql, bound):
    times = []
    for _ in range(3):
        t0 = time.perf_counter()
        conn.execute(sql, (bound,)).fetchone()
        times.append(time.perf_counter() - t0)
    return min(times) * 1e3


print("selected   index (ms)   scan (ms)")
for fraction in [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    bound = int(fraction * 100_000)
    seek = best_of_3("SELECT sum(pages) FROM loans INDEXED BY loans_day"
                     " WHERE out_day < ?", bound)
    scan = best_of_3("SELECT sum(pages) FROM loans NOT INDEXED"
                     " WHERE out_day < ?", bound)
    print(f"{fraction:8.1%} {seek:12.1f} {scan:11.1f}")
