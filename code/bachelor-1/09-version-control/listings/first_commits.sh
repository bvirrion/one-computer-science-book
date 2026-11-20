# capture: session
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
git init -q -b main catalogue
cd catalogue
printf 'The Silent Code,2002\nThe Paper Forest,1996\n' > books.csv
git add books.csv
git commit -q -m "Start the catalogue with two books"
printf 'Harbour Lights,2011\n' >> books.csv
git commit -q -am "Add Harbour Lights"
git log
git log --oneline
git show --stat HEAD
