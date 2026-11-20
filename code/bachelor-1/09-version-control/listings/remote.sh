# capture: session
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
git init -q -b main catalogue && cd catalogue # hidden
printf 'The Silent Code,2002\nThe Paper Forest,1996\n' > books.csv && git add books.csv && git commit -q -m "Start the catalogue with two books" # hidden
printf 'Harbour Lights,2011\n' >> books.csv && git commit -q -am "Add Harbour Lights" # hidden
cd ..
git init -q --bare -b main shared.git
cd catalogue
git remote add origin ../shared.git
git push -q origin main
cd ..
git clone -q shared.git colleague
cd colleague
printf 'Stone Bridge,1987\n' >> books.csv
git commit -q -am "Add Stone Bridge"
git push -q origin main
cd ../catalogue
git log --oneline
git pull -q origin main
git log --oneline
git branch -a
