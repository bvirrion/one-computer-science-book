"""The weekend problem: coverage and mutation analysis of the town's date library,
under its first test suite, then with the two new tests."""

import sys
from pathlib import Path

from coverage_tool import Coverage
from mutate import analyse, suite_of

first = suite_of("date_tests", lambda name: not name.startswith("test_new_"))
both = suite_of("date_tests")
sys.modules.pop("towndate", None)
with Coverage("towndate.py") as cov:
    first()
print("first suite, coverage:")
for key, value in cov.report().items():
    print(f"   {key:25} {value}")
import towndate  # noqa: E402,F401

for label, suite in [("first suite", first), ("with the new tests", both)]:
    results = analyse("towndate", Path("towndate.py"), suite)
    killed = sum(r[3] for r in results)
    print(f"{label}: {killed} of {len(results)} mutants killed")
    for line, before, after, dead in results:
        if not dead:
            print(f"   survived, line {line}: {before}  ->  {after}")
