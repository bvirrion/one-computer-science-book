# capture: session
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
git init -q -b main catalogue && cd catalogue # hidden
printf 'The Silent Code,2002\nThe Paper Forest,1996\n' > books.csv && git add books.csv && git commit -q -m "Start the catalogue with two books" # hidden
printf 'Harbour Lights,2011\n' >> books.csv && git commit -q -am "Add Harbour Lights" # hidden
git switch -q -c genres
sed -i 's/$/,mystery/' books.csv
git commit -q -am "Add a genre column"
git switch -q main
git merge genres
git switch -q -c sort-by-year
sort -t, -k2,2n books.csv > sorted.csv && mv sorted.csv books.csv
git commit -q -am "Sort the books by year"
git switch -q main
printf 'Stone Bridge,1987,history\n' >> books.csv
git commit -q -am "Add Stone Bridge"
git merge-base main sort-by-year
git merge --no-edit sort-by-year
git log --graph --oneline --all
cat books.csv
