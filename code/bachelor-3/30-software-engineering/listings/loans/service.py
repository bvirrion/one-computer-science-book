"""The use cases. The service depends on abstractions it is given: a repository,
a clock, a fine policy (a strategy) and listeners told of each event (observers)."""

from datetime import timedelta

from loans.model import LOAN_DAYS, MAX_LOANS, Loan, LoanError


def flat_fine(days_late):  # a fine policy: 20 cents a day
    return 20 * days_late


def capped_fine(days_late):  # another one: 20 cents a day, at most 5 euros
    return min(20 * days_late, 500)


class LoanService:
    def __init__(self, repo, clock, fine=flat_fine, listeners=()):
        self.repo, self.clock, self.fine = repo, clock, fine
        self.listeners = list(listeners)

    def _tell(self, event, loan):
        for listener in self.listeners:
            listener(event, loan)

    def borrow(self, reader, book):
        if self.repo.open_loan_of(book.isbn) is not None:
            raise LoanError(f"{book.title} is already on loan")
        if len(self.repo.open_loans_of(reader.card)) >= MAX_LOANS:
            raise LoanError(f"{reader.name} already has {MAX_LOANS} loans")
        today = self.clock()
        loan = Loan(book, reader, today, today + timedelta(days=LOAN_DAYS))
        self.repo.add(loan)
        self._tell("borrowed", loan)
        return loan

    def give_back(self, isbn):
        loan = self.repo.open_loan_of(isbn)
        if loan is None:
            raise LoanError(f"{isbn} is not on loan")
        loan.returned = self.clock()
        self.repo.save(loan)
        self._tell("returned", loan)
        return self.fine(loan.days_late(loan.returned))

    def renew(self, isbn, weeks):
        if not 1 <= weeks <= 4:
            raise LoanError("a renewal is 1 to 4 weeks")
        loan = self.repo.open_loan_of(isbn)
        if loan is None:
            raise LoanError(f"{isbn} is not on loan")
        if loan.days_late(self.clock()) > 0:
            raise LoanError("a late loan cannot be renewed")
        loan = loan.renewed(weeks)
        self.repo.save(loan)
        self._tell("renewed", loan)
        return loan
