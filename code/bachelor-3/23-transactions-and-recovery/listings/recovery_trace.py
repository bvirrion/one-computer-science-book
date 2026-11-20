"""recovery_trace.py -- the log of crash_all's workload as it stands at crash 21,
after page 3 is written, and what each pass of recovery does with it."""

from crash_all import expected, workload
from minidb import recover

db = workload()
log, pages = next(snap for kind, what, snap in db.events if (kind, what) == ("page", 3))
for r in log:
    fields = {
        k: v for k, v in r.items() if k not in ("lsn", "kind", "prev") and v is not None
    }
    print(
        f"{r['lsn']:>3} {r['kind']:<10} "
        + " ".join(f"{k}={v}" for k, v in fields.items())
    )
for p, q in pages.items():
    print(f"on disk, page {p}: {q['items']}, page LSN {q['lsn']}")
trace = []
values, full = recover(log, pages, trace)
print("\n".join(trace))
print("after recovery:", values)
print("expected:      ", expected(log))
