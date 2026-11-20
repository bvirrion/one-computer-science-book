"""The loan desk's command line: one command per line of standard input,
each with its date, so that a whole session can be replayed."""

import sys
from datetime import date

from catalogue import CatalogueAdapter, TownCatalogue
from loans.model import LoanError, Reader
from loans.repo import SqliteLoans
from loans.service import LoanService

READERS = {"C1": Reader("C1", "Ada"), "C2": Reader("C2", "Grace")}

today = date(2026, 1, 1)
books = CatalogueAdapter(TownCatalogue())
service = LoanService(SqliteLoans(), clock=lambda: today)
for line in sys.stdin:
    day, command, *args = line.split()
    today = date.fromisoformat(day)
    try:
        if command == "borrow":
            loan = service.borrow(READERS[args[0]], books.book(args[1]))
            print(f"{day} {loan.reader.name} borrows {loan.book.title}, due {loan.due}")
        elif command == "return":
            fine = service.give_back(args[0])
            print(f"{day} returned, fine {fine / 100:.2f} euros")
        elif command == "renew":
            loan = service.renew(args[0], int(args[1]))
            print(f"{day} {loan.book.title} renewed, due {loan.due}")
    except LoanError as e:
        print(f"{day} refused: {e}")
