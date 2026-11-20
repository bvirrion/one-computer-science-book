"""The chapter's pipelines and scripts, checked against Python computations."""

import csv
import os
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LISTINGS = HERE.parent / "listings"
EXERCISES = HERE.parent / "exercises"
TOWN = HERE.parents[3] / "data" / "town"
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
sys.path.insert(0, str(LISTINGS))

from log_check import check  # noqa: E402
from loans_check import top_members  # noqa: E402
from make_log import make_log  # noqa: E402


def sh(command, cwd):
    return subprocess.run(["bash", "-c", command], cwd=cwd, env=ENV, capture_output=True, text=True)


def test_hook_pipeline_equals_python():
    out = sh("tail -n +2 loans.csv | cut -d, -f3 | sort | uniq -c | sort -rn | head -5", TOWN).stdout
    top, distinct = top_members(TOWN / "loans.csv")
    assert out == "".join(f"{c:7d} {m}\n" for m, c in top)
    assert sh("tail -n +2 loans.csv | cut -d, -f3 | sort -u | wc -l", TOWN).stdout.strip() == str(distinct)


def test_log_pipelines_equal_python(tmp_path):
    (tmp_path / "access.log").write_text("\n".join(make_log()) + "\n", encoding="utf8")
    n, (hour, count), distinct = check(tmp_path / "access.log")
    top = sh("cut -c12-13 access.log | sort | uniq -c | sort -rn | head -1", tmp_path).stdout.split()
    assert top == [str(count), hour]
    members = sh("grep -oE 'member=[0-9]+' access.log | sort -u | wc -l", tmp_path).stdout.strip()
    assert members == str(distinct) and n == 640
    r = sh(f"bash {LISTINGS / 'logstat.sh'} access.log {hour}", tmp_path)
    assert r.returncode == 0 and r.stdout.startswith(f"hour {hour}: {count} lines")
    assert sh(f"bash {LISTINGS / 'logstat.sh'} access.log 07", tmp_path).returncode == 1
    assert sh(f"bash {LISTINGS / 'logstat.sh'} access.log 7", tmp_path).returncode == 2
    assert sh(f"bash {LISTINGS / 'logstat.sh'} access.log", tmp_path).returncode == 2


def test_topk_equals_python():
    out = sh(f"bash {EXERCISES / 'topk.sh'} weather.csv 2 3", TOWN).stdout.split("\n")
    with open(TOWN / "weather.csv", newline="", encoding="utf8") as f:
        counts = Counter(row["station"] for row in csv.DictReader(f))
    assert out[0].split() == [str(counts["Riverside"]), "Riverside"]
    assert out[1].split() == [str(counts["Hilltop"]), "Hilltop"]
    assert sh(f"bash {EXERCISES / 'topk.sh'} weather.csv x 3", TOWN).returncode == 2


def test_hottest_day_per_station():
    cmd = "tail -n +2 weather.csv | grep -vE ',,|,-99' | sort -t, -k3,3gr | sort -t, -k2,2 -s -u"
    out = sh(cmd, TOWN).stdout.splitlines()
    best = {}
    with open(TOWN / "weather.csv", newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            if row["temp_c"] in ("", "-99.0"):
                continue
            t = float(row["temp_c"])
            if row["station"] not in best or t > best[row["station"]][0]:
                best[row["station"]] = (t, row["date"])
    assert [line.split(",")[:3] for line in out] == [
        [best[s][1], s, f"{best[s][0]:.1f}"] for s in sorted(best)
    ]


def test_dupes(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "x.txt").write_text("rain\n")
    (tmp_path / "y.txt").write_text("rain\n")
    (tmp_path / "a" / "z with space.txt").write_text("rain\n")
    (tmp_path / "w.txt").write_text("wind\n")
    (tmp_path / "v.txt").write_text("snow\n")  # same size as w.txt, other content
    out = sh(f"bash {EXERCISES / 'dupes.sh'} .", tmp_path).stdout.splitlines()
    assert out == ["./a/x.txt|./a/z with space.txt|./y.txt"]


def test_octal_modes_counted():
    # exercise 9: the owner can read, and neither group nor others can write
    ok = [m for m in range(0o1000) if m & stat.S_IRUSR and not m & (stat.S_IWGRP | stat.S_IWOTH)]
    assert len(ok) == 64


def test_link_counts(tmp_path):
    # exercise 11: ln a b; ln -s a c; rm a
    a, b, c = tmp_path / "a", tmp_path / "b", tmp_path / "c"
    a.write_text("data\n")
    os.link(a, b)
    os.symlink("a", c)
    assert a.stat().st_nlink == 2 and b.stat().st_nlink == 2
    a.unlink()
    assert b.stat().st_nlink == 1 and b.read_text() == "data\n"
    assert c.is_symlink() and not c.exists()
