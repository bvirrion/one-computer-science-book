"""Exercise 5: a test of the fine that always passes, and its fix. Mutation testing
finds it: the mutants of the fine policy survive the first version."""

from datetime import date, timedelta

from loans.model import Book, Reader
from loans.repo import SqliteLoans
from loans.service import LoanService

DAY = date(2026, 3, 2)


def returned_four_days_late():
    today = [DAY]
    service = LoanService(SqliteLoans(), clock=lambda: today[0])
    loan = service.borrow(Reader("C1", "Ada"), Book("1", "Dune"))
    today[0] = DAY + timedelta(days=25)
    return loan, service.give_back("1")


def test_fine_always_passes():
    loan, fine = returned_four_days_late()
    assert (
        loan.days_late(DAY + timedelta(days=25)) == 4
    )  # checks the loan, not the fine


def test_fine_fixed():
    loan, fine = returned_four_days_late()
    assert fine == 80
