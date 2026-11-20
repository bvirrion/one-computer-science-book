"""Statement and branch coverage of loans/service.py under two test sets."""

import sys

from coverage_tool import Coverage
from mutate import suite_of

sys.path.insert(0, "../tests")
first_two = ("test_days_late_is_zero_until_due", "test_late_return_is_fined")
for label, keep in [
    ("the first two tests", lambda name: name in first_two),
    ("the whole suite", lambda name: "end_to_end" not in name),
]:
    for name in [m for m in sys.modules if m.startswith(("loans", "catalogue"))]:
        del sys.modules[name]  # import afresh, inside the measurement
    with Coverage("loans/service.py") as cov:
        passed = suite_of("test_loans", keep)()
    report = cov.report()
    print(f"{label}: {'all pass' if passed else 'a test fails'}")
    for key, value in report.items():
        print(f"   {key:25} {value}")
