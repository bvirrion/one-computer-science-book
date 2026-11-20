"""The loan system's tests: unit, integration and end to end, with test doubles."""

import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

from catalogue import CatalogueAdapter, TownCatalogue  # noqa: E402
from loans.model import Book, Loan, LoanError, Reader  # noqa: E402
from loans.repo import SqliteLoans  # noqa: E402
from loans.service import LoanService, capped_fine, flat_fine  # noqa: E402

ADA, GRACE = Reader("C1", "Ada"), Reader("C2", "Grace")
DUNE = Book("9780441013593", "Dune")
DAY = date(2026, 3, 2)


class Clock:  # a stub: the test sets the date
    def __init__(self, today):
        self.today = today

    def __call__(self):
        return self.today


def make_service(repo=None, fine=flat_fine):
    events = []  # a spy: the listener records what it was told
    clock = Clock(DAY)
    service = LoanService(
        repo or SqliteLoans(),
        clock,
        fine,
        [lambda event, loan: events.append((event, loan.book.isbn))],
    )
    return service, clock, events


def test_days_late_is_zero_until_due():  # a unit test: one class, no collaborator
    loan = Loan(DUNE, ADA, DAY, DAY + timedelta(days=21))
    assert loan.days_late(DAY + timedelta(days=21)) == 0
    assert loan.days_late(DAY + timedelta(days=24)) == 3


def test_late_return_is_fined():  # an integration test: service and SQLite together
    service, clock, events = make_service()
    service.borrow(ADA, DUNE)
    clock.today = DAY + timedelta(days=21 + 4)
    assert service.give_back(DUNE.isbn) == 80
    assert events == [("borrowed", DUNE.isbn), ("returned", DUNE.isbn)]


def test_a_book_cannot_be_borrowed_twice():
    service, _, _ = make_service()
    service.borrow(ADA, DUNE)
    with pytest.raises(LoanError, match="already on loan"):
        service.borrow(GRACE, DUNE)


def test_six_loans_are_refused():
    service, _, _ = make_service()
    for i in range(5):
        service.borrow(ADA, Book(f"isbn{i}", f"book {i}"))
    with pytest.raises(LoanError, match="already has 5 loans"):
        service.borrow(ADA, Book("isbn5", "book 5"))


def test_renewal_rules():
    service, clock, events = make_service()
    service.borrow(ADA, DUNE)
    with pytest.raises(LoanError, match="1 to 4 weeks"):
        service.renew(DUNE.isbn, 5)
    assert service.renew(DUNE.isbn, 2).due == DAY + timedelta(days=35)
    assert service.repo.open_loan_of(DUNE.isbn).due == DAY + timedelta(days=35)
    clock.today = DAY + timedelta(days=36)
    with pytest.raises(LoanError, match="late loan"):
        service.renew(DUNE.isbn, 1)
    with pytest.raises(LoanError, match="not on loan"):
        service.renew("nothing", 1)
    with pytest.raises(LoanError, match="not on loan"):
        service.give_back("nothing")


def test_fine_strategies():
    assert [flat_fine(d) for d in (0, 1, 30)] == [0, 20, 600]
    assert [capped_fine(d) for d in (0, 1, 30)] == [0, 20, 500]
    service, clock, _ = make_service(fine=capped_fine)
    service.borrow(ADA, DUNE)
    clock.today = DAY + timedelta(days=21 + 30)
    assert service.give_back(DUNE.isbn) == 500


def test_adapter():
    books = CatalogueAdapter(TownCatalogue())
    assert books.book("9780141439518") == Book("9780141439518", "Pride and Prejudice")
    with pytest.raises(KeyError):
        books.book("0000000000000")


def test_desk_end_to_end():  # the whole program, through its command line
    stdin = (HERE / "listings" / "desk.stdin").read_text()
    out = subprocess.run(
        [sys.executable, "desk.py"],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=HERE / "listings",
        check=True,
    ).stdout
    assert out.splitlines()[-1] == "2026-05-08 returned, fine 2.20 euros"
    assert out.count("refused") == 2
