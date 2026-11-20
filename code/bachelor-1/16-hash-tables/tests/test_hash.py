"""Word frequencies against Counter, the colliding strings, the additive counts."""

import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CH = HERE.parent
sys.path.insert(0, str(CH / "exercises"))

from additive_count import most_common, sums  # noqa: E402
from collide import colliding, poly  # noqa: E402

TEXT = """It was the best of times, it was the worst of times; it was the age of
wisdom, it was the age of foolishness. The town's library lends the best books."""


@pytest.mark.skipif(shutil.which("gcc") is None, reason="needs gcc")
def test_wordfreq(tmp_path):
    exe = tmp_path / "wordfreq"
    src = [CH / "exercises" / "wordfreq.c", CH / "listings" / "chain.c",
           CH / "listings" / "hashes.c"]
    subprocess.run(["gcc", "-std=c17", "-O2", "-Wall", "-Wextra", "-Werror",
                    "-I", str(CH / "listings"), *map(str, src), "-o", str(exe)],
                   check=True)
    out = subprocess.run([str(exe)], input=TEXT, capture_output=True, text=True,
                         check=True).stdout
    got = {w: int(c) for w, c in (line.split() for line in out.splitlines())}
    words = "".join(ch.lower() if ch.isalpha() else " " for ch in TEXT).split()
    assert got == Counter(words)


def test_colliding():
    for k, length in [(2, 2), (16, 8), (1000, 20)]:
        keys = colliding(k, length)
        assert len(set(keys)) == k and all(len(s) == length for s in keys)
        assert len({poly(s) for s in keys}) == 1


def test_additive():
    value, count, distinct = most_common()
    assert (value, count, distinct) == (438, 11726, 101)
    assert sum(sums().values()) == 26**4
    assert sums(2)[2 * ord("m")] == 25  # (a, y), (b, x), ..., (y, a)
