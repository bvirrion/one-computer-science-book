"""End-to-end test: build with make in a temporary folder, generate the corpus, and
compare search with the naive scan on the 200 seeded queries, outputs and exit
statuses; then the same queries under AddressSanitizer, which must stay silent."""

import shutil
import subprocess
import tempfile
from pathlib import Path

LISTINGS = Path(__file__).resolve().parents[1] / "listings"
SOURCES = ["Makefile", "make_corpus.py"] + sorted(
    p.name for p in LISTINGS.iterdir() if p.suffix in (".c", ".h"))


def build(folder, cflags=None):
    for name in SOURCES:
        shutil.copy(LISTINGS / name, folder)
    args = ["make", "-s", "search", "naive"] + ([f"CFLAGS={cflags}", f"LDLIBS=-lm {cflags}"]
                                                if cflags else [])
    subprocess.run(args, cwd=folder, check=True, capture_output=True)
    subprocess.run(["python3", "make_corpus.py", "corpus"], cwd=folder, check=True,
                   capture_output=True)
    return (folder / "queries.txt").read_text().splitlines()


def run(folder, program, words, env=None):
    return subprocess.run([f"./{program}", "corpus", *words], cwd=folder, env=env,
                          capture_output=True, text=True)


def test_search_agrees_with_the_naive_scan():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        queries = build(folder)
        statuses = set()
        for q in queries + ["quixotic", "Quartzite!", "xylograph quixotic", "zzz"]:
            a, b = run(folder, "search", q.split()), run(folder, "naive", q.split())
            assert (a.stdout, a.returncode) == (b.stdout, b.returncode), q
            statuses.add(a.returncode)
        assert statuses == {0, 1}
        assert run(folder, "search", ["quartzite"]).stdout.startswith("4 documents")
        nowhere = subprocess.run(["./search", "nowhere", "x"], cwd=folder,
                                 capture_output=True)
        assert nowhere.returncode == 2


def test_address_sanitizer_is_silent():
    flags = "-std=c17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        queries = build(folder, flags)
        env = {"PATH": "/usr/bin:/bin", "ASAN_OPTIONS": "detect_leaks=1"}
        for q in queries[:20] + ["", "zzz"]:
            r = run(folder, "search", q.split(), env)
            assert r.returncode in (0, 1) and r.stderr == "", r.stderr
