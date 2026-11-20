"""The loan system's data, and the rules that need nothing but the data."""

from dataclasses import dataclass
from datetime import date, timedelta

LOAN_DAYS = 21  # a loan lasts three weeks
MAX_LOANS = 5  # open loans per reader


@dataclass(frozen=True)
class Book:
    isbn: str
    title: str


@dataclass(frozen=True)
class Reader:
    card: str
    name: str


@dataclass
class Loan:
    book: Book
    reader: Reader
    start: date
    due: date
    returned: date | None = None

    def days_late(self, today: date) -> int:
        end = self.returned or today
        return max(0, (end - self.due).days)

    def renewed(self, weeks: int) -> "Loan":
        return Loan(
            self.book, self.reader, self.start, self.due + timedelta(weeks=weeks)
        )


class LoanError(Exception):
    """A use case refused: the message says why."""
