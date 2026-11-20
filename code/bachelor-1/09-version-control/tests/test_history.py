"""The generated history, its single bad commit, bisection, the exercise scripts."""

import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LISTINGS = HERE.parent / "listings"
EXERCISES = HERE.parent / "exercises"
sys.path.insert(0, str(LISTINGS))

from make_history import BAD, BRANCH, FORK, MAIN, make_history  # noqa: E402


def env(home):
    return {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": str(home),
            "PYTHONDONTWRITEBYTECODE": "1",
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}


def run(args, cwd, home):
    return subprocess.run(args, cwd=cwd, env=env(home), capture_output=True, text=True)


def git(cwd, *args):
    return run(["git", *args], cwd, cwd).stdout.split()


def history(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    make_history(str(repo))
    return repo


def test_shape(tmp_path):
    repo = history(tmp_path)
    assert len(git(repo, "rev-list", "HEAD")) == MAIN + BRANCH + 1 == 64
    assert len(git(repo, "rev-list", "--merges", "HEAD")) == 1
    assert len(git(repo, "rev-list", "--first-parent", "HEAD")) == MAIN + 1
    base = git(repo, "merge-base", "HEAD^1", "HEAD^2")[0]
    first_parent = git(repo, "rev-list", "--reverse", "--first-parent", "HEAD")
    assert first_parent.index(base) == FORK - 1


def test_exactly_one_bad_commit(tmp_path):
    repo = history(tmp_path)
    verdicts = {}
    for sha in git(repo, "rev-list", "HEAD"):
        run(["git", "checkout", "-q", sha], repo, repo)
        verdicts[sha] = run([sys.executable, "check.py"], repo, repo).returncode
    bad = [sha for sha, status in verdicts.items() if status != 0]
    first_parent = git(repo, "rev-list", "--reverse", "--first-parent", "main")
    # the bad commit and every main commit after it, the merge included
    assert set(bad) == set(first_parent[BAD - 1:])
    culprit = first_parent[BAD - 1]
    run(["git", "checkout", "-q", "main"], repo, repo)
    message = run(["git", "log", "-1", "--format=%s", culprit], repo, repo).stdout
    assert message == "Tidy the catalogue functions\n"


def test_bisect_run(tmp_path):
    repo = history(tmp_path)
    root = git(repo, "rev-list", "--max-parents=0", "HEAD")[0]
    run(["git", "bisect", "start", "HEAD", root], repo, repo)
    out = run(["git", "bisect", "run", sys.executable, "check.py"], repo, repo).stdout
    culprit = git(repo, "rev-list", "--reverse", "--first-parent", "main")[BAD - 1]
    assert f"{culprit} is the first 'bad' commit" in out
    assert out.count("running") <= math.ceil(math.log2(64))


def test_bisect_test_statuses(tmp_path):
    script = EXERCISES / "bisect_test.sh"
    check = "import sys\nsys.exit(int(open('verdict').read()))\n"
    (tmp_path / "check.py").write_text(check)
    for source, verdict, expected in [("x = 1\n", 0, 0), ("x = 1\n", 1, 1),
                                      ("def (\n", 0, 125), ("x = 1\n", 3, 125)]:
        (tmp_path / "catalogue.py").write_text(source)
        (tmp_path / "verdict").write_text(str(verdict))
        assert run(["bash", str(script)], tmp_path, tmp_path).returncode == expected


def test_touch_count(tmp_path):
    repo = history(tmp_path)
    script = str(LISTINGS / "touch_count.sh")
    out = run(["bash", script, str(repo)], tmp_path, tmp_path).stdout
    counts = {name: int(n) for n, name in map(str.split, out.splitlines())}
    expected = {"books.csv": MAIN - 1, "covers.csv": BRANCH,
                "catalogue.py": 2, "check.py": 1}
    assert counts == expected


def test_bisection_bound():
    # bisection over n candidates with good before bad needs at most ceil(log2 n) tests
    def worst(n):
        return 0 if n <= 1 else 1 + worst(n - n // 2)
    for n in range(1, 300):
        assert worst(n) == (math.ceil(math.log2(n)) if n > 1 else 0)
