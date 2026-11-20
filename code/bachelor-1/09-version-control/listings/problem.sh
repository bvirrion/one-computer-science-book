# capture: session copy=make_history.py
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-01-05T09:00:00+0000" GIT_COMMITTER_DATE="2026-01-05T09:00:00+0000" # hidden
python3 make_history.py repo
cd repo
git rev-list --count HEAD
git log --graph --oneline | sed -n '1,3p;25,27p;34,36p;45,48p;65,66p'
git log --oneline --merges
git rev-list --count --first-parent HEAD
git rev-list --count covers
git log --oneline -1 $(git merge-base HEAD^1 HEAD^2)
git rev-list --count HEAD ^covers
git rev-list --count covers ^HEAD^1
git log --oneline -1 -- catalogue.py
git diff HEAD~11 HEAD~10 -- catalogue.py | grep -E '^[-+] '
