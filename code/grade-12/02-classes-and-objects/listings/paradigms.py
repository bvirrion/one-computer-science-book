"""Total days late over the loans returned after their due date, three ways."""
import csv
from datetime import date

with open("loans.csv", newline="") as f:
    LOANS = list(csv.DictReader(f))


def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def is_late(loan):
    return loan["return_date"] != "" and loan["return_date"] > loan["due_date"]


# imperative: a variable changed step by step
total = 0
for loan in LOANS:
    if is_late(loan):
        total += days(loan["due_date"], loan["return_date"])
print("imperative:", total)

# functional: functions applied to whole sequences, no variable changed
lateness = map(lambda x: days(x["due_date"], x["return_date"]), filter(is_late, LOANS))
print("functional:", sum(lateness))


# object: each loan knows how late it is
class Loan:
    def __init__(self, row):
        self.due, self.returned = row["due_date"], row["return_date"]

    def days_late(self):
        if self.returned != "" and self.returned > self.due:
            return days(self.due, self.returned)
        return 0


print("object:", sum(Loan(row).days_late() for row in LOANS))
