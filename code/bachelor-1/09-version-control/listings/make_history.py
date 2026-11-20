"""make_history.py DIR: a 64-commit history of the catalogue, with one bad commit."""

import os
import random
import subprocess
import sys

CATALOGUE = '''"""catalogue.py: the library's catalogue."""


def load(path):
    with open(path, encoding="utf8") as f:
        rows = (line.rsplit(",", 1) for line in f if line.strip())
        return [(title, int(year)) for title, year in rows]


def oldest(books):
    return {fn}(books, key=lambda book: book[1])


def by_decade(books):
    counts = {{}}
    for _, year in books:
        counts[year // 10 * 10] = counts.get(year // 10 * 10, 0) + 1
    return counts
'''

CHECK = '''"""check.py: the catalogue's test; exit status 0 if it passes, 1 if not."""

import sys

from catalogue import by_decade, oldest

BOOKS = [("Harbour Lights", 2011), ("Stone Bridge", 1987), ("Silent Code", 2002)]
if oldest(BOOKS) != ("Stone Bridge", 1987):
    print("FAIL: oldest() returned", oldest(BOOKS))
    sys.exit(1)
if by_decade(BOOKS) != {1980: 1, 2000: 1, 2010: 1}:
    print("FAIL: by_decade() returned", by_decade(BOOKS))
    sys.exit(1)
print("ok")
'''

WORDS = ["Silent", "Paper", "Stone", "Harbour", "Winter",
         "Copper", "Hidden", "Northern", "Quiet", "Amber"]
NOUNS = ["Code", "Forest", "Bridge", "Lights", "Garden",
         "River", "Letter", "Map", "Tower", "Orchard"]
MAIN, BRANCH = 40, 23  # commits on main (before the merge), commits on the branch
FORK, BAD = 20, 31  # the branch starts after main commit 20; main commit 31 is bad


def make_history(where, seed=7):
    rng = random.Random(seed)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C",
           "HOME": where, "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_CONFIG_SYSTEM": os.devnull}
    for role in ("AUTHOR", "COMMITTER"):
        env[f"GIT_{role}_NAME"] = "Ada Lovelace"
        env[f"GIT_{role}_EMAIL"] = "ada@example.org"
    minute = 0

    def git(*args):
        nonlocal minute
        if args[0] in ("commit", "merge"):
            minute += 1
            hour, mins = 9 + minute // 60, minute % 60
            stamp = f"2026-01-05T{hour:02d}:{mins:02d}:00+0000"
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = stamp
        subprocess.run(["git", *args], cwd=where, env=env,
                       check=True, capture_output=True)

    def write(name, text, mode="w"):
        with open(os.path.join(where, name), mode, encoding="utf8") as f:
            f.write(text)

    def a_book():
        year = rng.randint(1950, 2025)
        return f"The {rng.choice(WORDS)} {rng.choice(NOUNS)},{year}\n"

    git("init", "-q", "-b", "main")
    write("catalogue.py", CATALOGUE.format(fn="min"))
    write("check.py", CHECK)
    write("books.csv", a_book())
    git("add", ".")
    git("commit", "-q", "-m", "Start the catalogue")
    for i in range(2, MAIN + 1):
        if i == BAD:
            write("catalogue.py", CATALOGUE.format(fn="max"))
            git("commit", "-q", "-am", "Tidy the catalogue functions")
        else:
            title = a_book()
            write("books.csv", title, "a")
            git("commit", "-q", "-am", f"Add {title.rsplit(',', 1)[0]}")
        if i == FORK:
            git("branch", "covers")
    git("switch", "-q", "covers")
    for _ in range(BRANCH):
        line = f"{rng.randint(1, 40)},cover-{rng.randint(100, 999)}.jpg\n"
        write("covers.csv", line, "a")
        git("add", "covers.csv")
        book = line.split(",")[0]
        git("commit", "-q", "-m", f"Add a cover for book {book}")
    git("switch", "-q", "main")
    git("merge", "-q", "--no-edit", "covers")


if __name__ == "__main__":
    os.makedirs(sys.argv[1], exist_ok=True)
    make_history(os.path.abspath(sys.argv[1]))
