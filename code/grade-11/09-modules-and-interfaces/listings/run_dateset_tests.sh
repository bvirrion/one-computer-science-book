# capture: session copy=dateset_list.py,dateset_set.py,dateset_sorted.py,dateset_tests.py
python dateset_tests.py list 2>&1 | grep -v '^Ran '
python dateset_tests.py set 2>&1 | grep -v '^Ran '
