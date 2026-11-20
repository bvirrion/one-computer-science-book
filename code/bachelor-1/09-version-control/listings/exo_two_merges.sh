# capture: session
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
git init -q -b main catalogue && cd catalogue # hidden
printf 'The Silent Code,2002\nThe Paper Forest,1996\n' > books.csv && git add books.csv && git commit -q -m "Start the catalogue with two books" # hidden
printf 'Harbour Lights,2011\n' >> books.csv && git commit -q -am "Add Harbour Lights" # hidden
git switch -q -c a && printf 'A,2001\n' >> books.csv && git commit -q -am "A1" # hidden
git switch -q main && git switch -q -c b && printf 'b\n' > b.txt && git add b.txt && git commit -q -am "B1" # hidden
git switch -q main && printf 'x\n' > m.txt && git add m.txt && git commit -q -m "M1" # hidden
git merge -q --no-edit a
git merge -q --no-edit b
git log --graph --oneline
