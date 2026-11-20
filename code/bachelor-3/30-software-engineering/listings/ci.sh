# capture: session copy=towndate.py,date_tests.py,coverage_tool.py,gate.py
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-03-02T09:00:00+0000" GIT_COMMITTER_DATE="2026-03-02T09:00:00+0000" # hidden
git init -q -b main
printf '#!/bin/sh\nruff check -q . && python gate.py towndate.py date_tests 100\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
git add . && git commit -q -m "Town date library with its tests" && echo committed
sed -i 's/year % 100 != 0 or year % 400 == 0/True/' towndate.py
git commit -q -am "Simplify is_leap" || echo "commit refused"
sed -i 's/(True)/(year % 100 != 0 or year % 400 == 0)/' towndate.py
printf 'def test_new_1700():\n    assert not is_leap(1700)\n' >> date_tests.py
git commit -q -am "Test the year 1700" && echo committed
git log --oneline
