"""Problem: the corrected 2025 weather record of the two stations."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from load_weather import read_table  # noqa: E402

PATH = Path(__file__).parent.parent / "listings" / "weather.csv"


def clean(rows):
    """Drop missing values, the -99.0 code and repeated (date, station) records."""
    seen, kept = set(), []
    for r in rows:
        key = (r["date"], r["station"])
        if key not in seen and r["temp_c"] is not None and r["temp_c"] != -99.0:
            kept.append(r)
        seen.add(key)
    return kept


def mean(values):
    return sum(values) / len(values)


def monthly(rows, station):
    groups = {}
    for r in rows:
        if r["station"] == station and r["temp_c"] is not None:
            groups.setdefault(r["date"][5:7], []).append(r["temp_c"])
    return {m: mean(v) for m, v in sorted(groups.items())}


if __name__ == "__main__":
    rows = read_table(PATH)
    good = clean(rows)
    for station in ("Hilltop", "Riverside"):
        raw = [r["temp_c"] for r in rows
               if r["station"] == station and r["temp_c"] is not None]
        ok = [r["temp_c"] for r in good if r["station"] == station]
        months = monthly(good, station)
        warm = max(months, key=months.get)
        print(f"{station}: raw {mean(raw):.3f} ({len(raw)}), clean {mean(ok):.3f}"
              f" ({len(ok)}), error {mean(ok) - mean(raw):+.3f}")
        print(f"  warmest month {warm}: {months[warm]:.2f}")
    codes = [r["temp_c"] for r in rows if r["temp_c"] == -99.0]
    ok = [r["temp_c"] for r in good if r["station"] == "Riverside"]
    print(f"Riverside with the codes only: {mean(ok + codes):.3f}")
