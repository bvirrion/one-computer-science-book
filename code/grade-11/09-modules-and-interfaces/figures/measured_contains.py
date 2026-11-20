"""Write measured_contains.dat: microseconds per contains(s, d), three ways."""
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
import dateset_list  # noqa: E402
import dateset_set  # noqa: E402
import dateset_sorted  # noqa: E402
from measure_dateset import START, per_lookup  # noqa: E402

with open(Path(__file__).with_suffix(".dat"), "w") as out:
    out.write("n list sorted set\n")
    for n in [1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000]:
        days = [START + timedelta(days=2 * i) for i in range(n)]
        targets = [days[-1], days[-1] - timedelta(days=1)]
        row = [per_lookup(ds, ds.from_dates(days), targets) * 1e6
               for ds in (dateset_list, dateset_sorted, dateset_set)]
        out.write(f"{n} " + " ".join(f"{t:.3f}" for t in row) + "\n")
