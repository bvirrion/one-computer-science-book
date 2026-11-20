# capture: session
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
git init -q -b main catalogue && cd catalogue # hidden
printf 'The Silent Code,2002\nThe Paper Forest,1996\n' > books.csv && git add books.csv && git commit -q -m "Start the catalogue with two books" # hidden
printf 'Harbour Lights,2011\n' >> books.csv && git commit -q -am "Add Harbour Lights" # hidden
git switch -q -c rename
sed -i 's/The Paper Forest/The Paper Forest (2nd ed.)/' books.csv
git commit -q -am "Name the second edition"
git switch -q main
sed -i 's/The Paper Forest,1996/The Paper Forest,1997/' books.csv
git commit -q -am "Fix the year of The Paper Forest"
git merge rename
git status --short
cat books.csv
printf 'The Silent Code,2002\nThe Paper Forest (2nd ed.),1997\nHarbour Lights,2011\n' > books.csv
git add books.csv
git commit -q --no-edit
git log --oneline --graph
