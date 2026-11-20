# capture: session copy=leap.py,leap_fixed.py,leap_tests.py
python leap_tests.py 2>&1 | grep -v '^Ran '
python leap_tests.py fixed 2>&1 | grep -v '^Ran '
