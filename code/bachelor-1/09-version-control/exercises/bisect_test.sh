#!/bin/bash
# bisect_test.sh: the test for `git bisect run`: 0 good, 1 bad, 125 untestable.
if ! python3 -c 'import ast; ast.parse(open("catalogue.py").read())' 2> /dev/null; then
    exit 125                # the program does not even parse: no verdict, skip
fi
python3 check.py > /dev/null 2>&1
status=$?
case $status in
    0) exit 0 ;;            # the test passes: good
    1) exit 1 ;;            # the test fails: bad
    *) exit 125 ;;          # anything else is not a verdict on the bug
esac
