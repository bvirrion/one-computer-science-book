"""Exercise 6: an in-memory LoanRepository, a test double for SqliteLoans, and one set
of contract tests that every repository must pass."""

from dataclasses import replace


class MemoryLoans:
    def __init__(self):
        self.loans = []  # every loan, open or returned, in the order added

    def add(self, loan):
        self.loans.append(replace(loan))  # a copy: the caller's object is not stored

    def save(self, loan):
        for i, old in enumerate(self.loans):
            if old.book.isbn == loan.book.isbn and old.returned is None:
                self.loans[i] = replace(loan)
                return

    def open_loan_of(self, isbn):
        found = [x for x in self.loans if x.book.isbn == isbn and x.returned is None]
        return replace(found[0]) if found else None

    def open_loans_of(self, card):
        return [
            replace(x)
            for x in self.loans
            if x.reader.card == card and x.returned is None
        ]
