"""Grade 7, chapter 2: the lists match the town data, and the programs print what the text says."""

import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / "listings"))

import hilltop_2025  # noqa: E402
import rain  # noqa: E402


def town_rain():
    with open(ROOT / "data" / "town" / "weather.csv", newline="") as f:
        return [(r["date"], float(r["rain_mm"])) for r in csv.DictReader(f) if r["station"] == "Hilltop"]


def out(folder, name):
    r = subprocess.run([sys.executable, name], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def lines(folder, name):
    code, o, _ = out(folder, name)
    assert code == 0
    return o


def test_lists_equal_the_town_data():
    year = town_rain()
    assert rain.rain == [v for d, v in year if d.startswith("2025-01")]
    assert hilltop_2025.rain == [v for _, v in year]
    assert sum(hilltop_2025.month_days) == 365 == len(hilltop_2025.rain)
    assert (HERE / "exercises" / "rain.py").read_bytes() == (HERE / "listings" / "rain.py").read_bytes()


def test_listings():
    r = rain.rain
    assert lines("listings", "rain.py")[1:] == ["1 January: 0.0 mm", "12 January: 16.1 mm", "31 January: 0.0 mm"]
    code, o, err = out("listings", "index_error.py")
    assert code == 1 and o == ["0.0"] and "IndexError" in err
    assert lines("listings", "total_max_count.py") == [
        f"total: {round(sum(r), 1)} mm", f"wettest day: {max(r)} mm", f"dry days: {r.count(0.0)}"
    ]
    assert lines("listings", "position_of_max.py") == [f"wettest day: January {r.index(max(r)) + 1} with {max(r)} mm"]
    assert lines("listings", "shopping.py")[-1] == "['six eggs', 'bread']"
    assert lines("listings", "in_place.py")[-1] == "[0.7, 6.9, 3.3] 3"


def longest_dry(values):
    best, best_end, run = 0, 0, 0
    for i, v in enumerate(values):
        run = run + 1 if v == 0 else 0
        if run > best:
            best, best_end = run, i
    return best, best_end - best + 1


def test_dry_spells():
    n, start = longest_dry(rain.rain)
    assert lines("listings", "dry_spell.py") == [f"longest dry run: {n} days, from January {start + 1}"]
    n, start = longest_dry(hilltop_2025.rain)
    o = lines("listings", "dry_year.py")
    assert o[1] == f"longest dry spell: {n} days"
    assert all(v == 0 for v in hilltop_2025.rain[start:start + n])
    assert hilltop_2025.rain[start - 1] > 0 and hilltop_2025.rain[start + n] > 0
    year = town_rain()
    d0, d1 = year[start][0], year[start + n - 1][0]
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    assert o[2] == f"from {int(d0[8:])} {months[int(d0[5:7]) - 1]} to {int(d1[8:])} {months[int(d1[5:7]) - 1]}"


def test_exercise_solutions():
    r = rain.rain
    assert lines("exercises", "three_ops.py") == ["[2, 9, 3, 4]"]
    assert lines("exercises", "average.py") == [f"average: {round(sum(r) / 31, 2)} mm a day"]
    code, o, err = out("exercises", "off_by_one.py")
    assert code == 1 and len(o) == 4 and "IndexError" in err
    assert lines("exercises", "largest_bug.py") == ["0"]
    assert lines("exercises", "largest_fixed.py") == ["-1"]
    assert lines("exercises", "rainy_days.py") == [f"rainy days: {31 - r.count(0.0)}"]
    assert lines("exercises", "above5.py") == [str([v for v in r if v > 5])]
    assert lines("exercises", "reverse.py") == ["[0.3, 0.0, 6.9, 0.0, 0.7, 0.0, 0.0]"]
    for line in lines("exercises", "longest_equal.py"):
        expected, got = line.removeprefix("expected ").split(", got ")
        assert expected == got
