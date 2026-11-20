"""Mutation analysis of loans/service.py under the test suite (end-to-end test left out:
it runs the program in another process, which would not see the mutant)."""

import sys
from pathlib import Path

from mutate import analyse, suite_of

sys.path.insert(0, "../tests")
import loans.service  # noqa: E402,F401  (the real module, put back after the analysis)

results = analyse(
    "loans.service",
    Path("loans/service.py"),
    suite_of("test_loans", lambda name: "end_to_end" not in name),
)
killed = sum(r[3] for r in results)
score = killed / len(results)
print(f"{len(results)} mutants, {killed} killed, mutation score {score:.0%}")
for line, before, after, dead in results:
    if not dead:
        print(f"   survived, line {line}: {before}  ->  {after}")
