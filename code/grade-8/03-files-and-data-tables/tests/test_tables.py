"""Grade 8, chapter 3: files and data tables."""

import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"


def table(name):
    with open(LISTINGS / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lines(name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=LISTINGS, capture_output=True, text=True)
    assert r.returncode == 0
    return r.stdout.splitlines()


BOOKS, LOANS, WEATHER = table("books.csv"), table("loans.csv"), table("weather.csv")


def test_listings():
    assert lines("read_lines")[0] == f"{len(BOOKS) + 1} lines"
    assert lines("still_out")[0] == f"400 loans, {sum(r['return_date'] == '' for r in LOANS)} still out"
    longest = max(BOOKS, key=lambda b: int(b["pages"]))
    assert lines("longest_book") == [f"{longest['title']} by {longest['author']} - {longest['pages']} pages"]
    temps = [float(r["temp_c"]) for r in WEATHER if r["station"] == "Hilltop" and r["temp_c"]]
    assert -99.0 not in temps
    assert lines("mean_temp")[1] == f"mean temperature: {round(sum(temps) / len(temps), 2)} degrees"


def test_weather_problem():
    hill = [r for r in WEATHER if r["station"] == "Hilltop"]
    rain = {}
    for r in hill:
        rain[r["date"][5:7]] = rain.get(r["date"][5:7], 0) + float(r["rain_mm"])
    wettest = max(rain, key=rain.get)
    assert lines("weather_year")[-2] == f"wettest month: {wettest} with {round(rain[wettest], 1)} mm"
    river = [r for r in WEATHER if r["station"] == "Riverside"]
    values = [float(r["temp_c"]) for r in river if r["temp_c"]]
    good = [v for v in values if v != -99.0]
    out = lines("defects")
    assert out[0] == f"Riverside: {len(river)} rows, {len(river) - len(values)} missing, {values.count(-99.0)} codes"
    assert out[2].endswith(str(round(sum(values) / len(values), 2)))
    assert out[3].endswith(str(round(sum(good) / len(good), 2)))
    assert len(WEATHER) == 731


def test_exercises(tmp_path):
    counts = load("genres").count_genres(BOOKS)
    assert sum(counts.values()) == len(BOOKS)
    try:
        load("pages_bug").total_pages(BOOKS)
        raise AssertionError("the bug should raise")
    except TypeError:
        pass
    assert load("pages_fixed").total_pages(BOOKS) == sum(int(b["pages"]) for b in BOOKS)
    member, n = load("most_loans").most_loans(LOANS)
    per = {}
    for loan in LOANS:
        per[loan["member_id"]] = per.get(loan["member_id"], 0) + 1
    assert n == max(per.values()) and per[member] == n
    late = load("late").late_returns(LOANS)
    assert late == sum(1 for r in LOANS if r["return_date"] and r["return_date"] > r["due_date"])
    target = tmp_path / "poetry.csv"
    load("write_genre").write_genre(BOOKS, "poetry", target)
    with open(target, encoding="utf-8") as f:
        written = list(csv.DictReader(f))
    assert written == [b for b in BOOKS if b["genre"] == "poetry"]
    assert load("rainiest_week").rainiest_week(WEATHER, "Riverside") == ("2025-01-13", 36.9)
    assert "a,b,,c".split(",") == ["a", "b", "", "c"]
    assert "2025-01-09" < "2025-01-10" and "09-02-2025" < "10-01-2025"  # 9 February sorts before 10 January
