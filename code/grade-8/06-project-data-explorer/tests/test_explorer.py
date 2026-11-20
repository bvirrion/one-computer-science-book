"""Grade 8, project: the data explorer, its functions on the copied town tables."""

import csv
import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"
TOWN = HERE.parents[2] / "data" / "town"
sys.path.insert(0, str(LISTINGS))

import explorer_v5 as ex  # noqa: E402

BOOKS = ex.load_table(LISTINGS / "books.csv")
LOANS = ex.load_table(LISTINGS / "loans.csv")


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tables_and_counts():
    assert len(BOOKS) == ex.count_lines(LISTINGS / "books.csv") == 80
    assert len(LOANS) == ex.count_lines(LISTINGS / "loans.csv") == 400
    counts = ex.loans_by_genre(BOOKS, LOANS)
    assert sum(counts.values()) == len(LOANS)
    assert ex.never_borrowed(BOOKS, LOANS) == []
    top = ex.top_ten(BOOKS, LOANS)
    assert len(top) == 10 and top[0] == {"title": "The Clockwork Engine", "loans": 10}
    assert [ex.most_borrowed_first(r) for r in top] == sorted(
        ex.most_borrowed_first(r) for r in top)


def test_dates_and_report(tmp_path):
    assert ex.is_date("2025-06-30") and not ex.is_date("30/6/2025")
    assert not ex.is_date("2025-ab-30")
    assert len(ex.still_out_on(LOANS, "2025-06-30")) == 35
    end = ex.still_out_on(LOANS, "2025-12-31")
    assert len(end) == 24
    assert sum(1 for r in LOANS if r["return_date"] == "") == 22
    assert sum(1 for r in LOANS if r["return_date"] > "2025-12-31") == 2
    ex.save_report(["a", "b"], tmp_path / "r.txt")
    assert (tmp_path / "r.txt").read_text() == "a\nb\n"


def test_menu_session(monkeypatch):
    typed = iter(["5", "1", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(typed))
    spec = importlib.util.spec_from_file_location("v1", LISTINGS / "explorer_v1.py")
    v1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v1)
    with redirect_stdout(io.StringIO()) as out:
        v1.main()
    assert out.getvalue().splitlines()[-3:] == [
        "please type a number from 0 to 4", "question 1 is not ready yet", "goodbye"]


def test_exercises(tmp_path):
    toy = [{"book_id": "1", "title": "Ash"}, {"book_id": "2", "title": "Birch"},
           {"book_id": "3", "title": "Cedar"}]
    toy_loans = [{"book_id": i} for i in ["2", "3", "2", "1", "3"]]
    assert [r["title"] for r in ex.top_ten(toy, toy_loans)][:3] == ["Birch", "Cedar", "Ash"]
    author = BOOKS[0]["author"]
    assert load("by_author").books_by(BOOKS, author) == [
        b["title"] for b in BOOKS if b["author"] == author]
    bug = load("top_ten_bug").top_ten(BOOKS, LOANS)
    assert [r["title"] for r in bug[:2]] == ["The Clockwork Engine"] * 2
    assert load("busiest_month").busiest_month(LOANS) == ("09", 45)
    with open(TOWN / "members.csv", encoding="utf-8") as f:
        members = list(csv.DictReader(f))
    assert len(members) == 60 and load("never_borrowers").never_borrowers(members, LOANS) == []
    out = sum(1 for r in LOANS if r["out_date"] <= "30/6/2025" and (
        r["return_date"] == "" or r["return_date"] > "30/6/2025"))
    assert out == 22
    load("save_csv").save_csv(ex.top_ten(BOOKS, LOANS), tmp_path / "top.csv")
    assert (tmp_path / "top.csv").read_text().splitlines()[:2] == [
        "title,loans", "The Clockwork Engine,10"]
    assert load("loan_length").average_length(LOANS) == 17.6
    shuffled = LOANS[::-1]
    assert ex.top_ten(BOOKS, shuffled) == ex.top_ten(BOOKS, LOANS)
    assert load("best_pair").best_pair(LOANS) == ("5+47", 3)
