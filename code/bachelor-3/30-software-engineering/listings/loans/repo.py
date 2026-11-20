"""Where loans are kept. The service sees only the LoanRepository interface;
SqliteLoans is one implementation, a test double can be another."""

import sqlite3
from datetime import date
from typing import Protocol

from loans.model import Book, Loan, Reader


class LoanRepository(Protocol):
    def add(self, loan: Loan) -> None: ...
    def save(self, loan: Loan) -> None: ...
    def open_loan_of(self, isbn: str) -> Loan | None: ...
    def open_loans_of(self, card: str) -> list[Loan]: ...


class SqliteLoans:
    """Loans in an SQLite table: one row per loan, `returned` NULL while it is open."""

    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS loans (isbn TEXT, title TEXT, card TEXT,"
            " name TEXT, start TEXT, due TEXT, returned TEXT)"
        )

    def add(self, loan):
        self.db.execute(
            "INSERT INTO loans VALUES (?, ?, ?, ?, ?, ?, ?)", self._row(loan)
        )

    def save(self, loan):
        row = self._row(loan)
        self.db.execute(
            "UPDATE loans SET due = ?, returned = ?"
            " WHERE isbn = ? AND returned IS NULL",
            (row[5], row[6], loan.book.isbn),
        )

    def open_loan_of(self, isbn):
        rows = self._select("isbn = ?", isbn)
        return rows[0] if rows else None

    def open_loans_of(self, card):
        return self._select("card = ?", card)

    def _select(self, where, value):
        sql = f"SELECT * FROM loans WHERE {where} AND returned IS NULL ORDER BY start"
        return [self._loan(r) for r in self.db.execute(sql, (value,))]

    @staticmethod
    def _row(loan):
        returned = loan.returned.isoformat() if loan.returned else None
        return (
            loan.book.isbn,
            loan.book.title,
            loan.reader.card,
            loan.reader.name,
            loan.start.isoformat(),
            loan.due.isoformat(),
            returned,
        )

    @staticmethod
    def _loan(r):
        day = date.fromisoformat
        return Loan(
            Book(r[0], r[1]),
            Reader(r[2], r[3]),
            day(r[4]),
            day(r[5]),
            day(r[6]) if r[6] else None,
        )
