"""The town's old catalogue, which the library cannot change, and an adapter that
gives it the interface the loan system expects: book(isbn) -> Book."""

from loans.model import Book

RECORDS = {
    "9780140449136": "9780140449136|Crime and Punishment|F-DOS",
    "9780141439518": "9780141439518|Pride and Prejudice|F-AUS",
    "9780262033848": "9780262033848|Introduction to Algorithms|005.1-COR",
}


class TownCatalogue:  # the existing interface: one record as a "|"-separated line
    def fetch_record(self, code):
        return RECORDS.get(code, "")


class CatalogueAdapter:  # the interface the loan system wants
    def __init__(self, catalogue):
        self.catalogue = catalogue

    def book(self, isbn):
        record = self.catalogue.fetch_record(isbn)
        if not record:
            raise KeyError(isbn)
        code, title, _shelf = record.split("|")
        return Book(code, title)
