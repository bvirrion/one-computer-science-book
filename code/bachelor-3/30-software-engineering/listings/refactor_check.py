"""A characterisation test, run as a program: the old report on a sample of loans is
recorded, and the refactored code must print exactly the same, for several policies."""

from datetime import date

import refactor_after as after
import refactor_before as before

LOANS = [
    ("Dune", "Ada", date(2026, 3, 2)),
    ("Emma", "Grace", date(2026, 2, 9)),
    ("Ulysses", "Alan", date(2026, 3, 20)),
    ("Middlemarch", "Ada", date(2026, 1, 5)),
]
TODAY = date(2026, 3, 23)
print(before.fines_report(LOANS, TODAY, 20, 500, 2, "EUR"))
for rate, cap, grace in [(20, 500, 2), (20, None, 0), (35, 300, 7), (10, 0, 0)]:
    old = before.fines_report(LOANS, TODAY, rate, cap, grace, "EUR")
    new = after.fines_report(LOANS, TODAY, after.FinePolicy(rate, cap, grace, "EUR"))
    verdict = "same" if old == new else "DIFFERENT"
    print(f"rate {rate}, cap {cap}, grace {grace}: {verdict}")
