# the time on the line "Ran 6 tests in ..." changes from run to run: it is filtered out
python planner_tests.py 2>&1 | grep -v '^Ran '
