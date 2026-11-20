import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / "listings"))
sys.path.insert(0, str(HERE / "exercises"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


lw = load("listings", "load_weather")
weather = lw.read_table(HERE / "listings" / "weather.csv")
loans = lw.read_table(HERE / "listings" / "loans.csv")


def test_copies_match_town_tables():
    for name in ("weather", "loans", "books", "members", "people"):
        copy = (HERE / "listings" / f"{name}.csv").read_bytes()
        assert copy == (ROOT / "data" / "town" / f"{name}.csv").read_bytes()


def test_convert():
    assert lw.convert("") is None and lw.convert("12") == 12
    assert lw.convert("-99.0") == -99.0 and lw.convert("Hilltop") == "Hilltop"


def test_table_tools():
    t = load("exercises", "table_tools")
    rows = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}, {"a": 3, "b": "x"}]
    assert t.project(rows, ["b"]) == [{"b": "x"}, {"b": "y"}, {"b": "x"}]
    assert t.group_count(rows, "b") == {"x": 2, "y": 1}
    assert t.median_by(rows, "b", "a") == {"x": 2.0, "y": 2}
    members = [{"m": 1}, {"m": 2}]
    lo = [{"m": 1, "book": 5}, {"m": 1, "book": 6}]
    assert t.left_join(members, lo, "m") == [
        {"m": 1, "book": 5}, {"m": 1, "book": 6}, {"m": 2, "book": None}]


def test_bugs():
    b = load("exercises", "bugs")
    rows = [{"year": "10"}, {"year": "9"}]
    assert [r["year"] for r in b.sort_years_buggy(rows)] == ["10", "9"]
    assert [r["year"] for r in b.sort_years(rows)] == ["9", "10"]
    lines = ["2025-06-14,Riverside,21.5", "2025-06-14, Riverside,21.5"]
    assert b.duplicates_buggy(lines) == [] and b.duplicates(lines) == [lines[1]]
    assert b.mean([1.0, None, -99.0, 3.0]) == 2.0
    assert b.mean_buggy([1.0, None, -99.0, 3.0]) < 0


def test_check_loans_clean_and_broken():
    c = load("exercises", "check_loans")
    assert c.problems(loans) == []
    bad = [{"loan_id": 1, "out_date": "2025-01-10", "due_date": "2025-01-30",
            "return_date": "2025-01-09"}]
    assert [m for _, m in c.problems(bad)] == [
        "due date is not 21 days after", "returned before it went out"]


def test_json_round_trip():
    j = load("exercises", "json_roundtrip")
    members = lw.read_table(HERE / "listings" / "members.csv")
    data = j.members_with_loans(members, loans)
    assert len(data) == 60 and sum(len(m["loans"]) for m in data) == 400
    assert j.round_trip(data)


def test_corrected_weather():
    cw = load("exercises", "corrected_weather")
    good = cw.clean(weather)
    assert len(good) == 731 - 6 - 2 - 1
    river = [r["temp_c"] for r in good if r["station"] == "Riverside"]
    assert round(cw.mean(river), 3) == 12.016


def test_monthly_means_dat():
    fig = load("figures", "monthly_means")
    fig.main()
    lines = fig.OUT.read_text().splitlines()
    assert len(lines) == 13 and lines[1].startswith("1 0.648 3.970")


def test_left_join_on_town_tables():
    t = load("exercises", "table_tools")
    members = lw.read_table(HERE / "listings" / "members.csv")
    books = lw.read_table(HERE / "listings" / "books.csv")
    joined = t.left_join(members, loans, "member_id")
    assert len(joined) == 400 and all(r["loan_id"] is not None for r in joined)
    assert all(r["loan_id"] is not None for r in t.left_join(books, loans, "book_id"))
