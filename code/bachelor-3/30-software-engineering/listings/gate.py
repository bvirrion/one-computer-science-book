"""The project's check before each commit: run the tests under the coverage tool,
name the failing tests, and fail if statement coverage is below a threshold.
Usage: python gate.py MODULE.py TEST_MODULE MIN_PERCENT"""

import sys

from coverage_tool import Coverage

module, tests, minimum = sys.argv[1], sys.argv[2], float(sys.argv[3])
failed = []
with Coverage(module) as cov:
    suite = __import__(tests)  # imports the module under test, inside the measurement
    for name in sorted(n for n in dir(suite) if n.startswith("test_")):
        try:
            getattr(suite, name)()
        except AssertionError:
            failed.append(name)
report = cov.report()
run, total = report["statements"]
taken, branches = report["branches"]
print(
    f"gate: {len(failed)} failed: {', '.join(failed) or '-'}; "
    f"statements {run}/{total}, branches {taken}/{branches}"
)
if failed or 100 * run < minimum * total:
    print("gate: refused")
    sys.exit(1)
