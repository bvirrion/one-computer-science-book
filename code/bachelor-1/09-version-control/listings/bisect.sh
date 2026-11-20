# capture: session copy=make_history.py
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
python3 make_history.py repo
cd repo
git rev-list --count HEAD
python3 check.py; echo "exit status $?"
git bisect start HEAD $(git rev-list --max-parents=0 HEAD)
git bisect run python3 check.py
git bisect reset
