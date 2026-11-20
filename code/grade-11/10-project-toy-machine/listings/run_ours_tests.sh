# the time on the line "Ran 4 tests in ..." changes from run to run: it is filtered out
python ours_tests.py 2>&1 | grep -v '^Ran '
