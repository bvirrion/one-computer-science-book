# capture: scratch
"""make_corpus.py: a seeded folder of 400 invented texts for the search engine, and
200 queries. Word frequencies follow a Zipf-like law: the word of rank r is drawn with
probability proportional to 1 / r. A few rare words are planted for the tests."""

import random
import sys
from collections import Counter
from pathlib import Path

SYLLABLES = [c + v for c in "bdfghklmnprstvw" for v in "aeiou"]  # no q, x, y or z
PLANTED = {"quixotic": [7, 211], "xylograph": [42], "quartzite": [3, 99, 250, 391]}


def vocabulary(rng, size=5000):
    words = set()
    while len(words) < size:
        words.add("".join(rng.choice(SYLLABLES) for _ in range(rng.randint(1, 4))))
    return sorted(words, key=lambda w: (len(w), w))  # short words get the high ranks


def document(rng, words, weights, doc):
    n = rng.randint(200, 2000)
    text = rng.choices(words, weights, k=n)
    for word, docs in PLANTED.items():
        if doc in docs:
            text[rng.randrange(n)] = word
    if doc % 50 == 0:
        text[0] = "Café"  # a non-ASCII letter: the tokenizer splits it
    lines, line = [], []
    for i, w in enumerate(text):
        end = "." if i % 12 == 11 else ""  # sentences of twelve words
        line.append(w.capitalize() if i % 12 == 0 else w + end)
        if len(line) == 10:
            lines.append(" ".join(line))
            line = []
    lines.append(" ".join(line))
    end = "" if doc % 40 == 1 else "\n"  # some files have no final newline
    return "\n".join(lines) + end, text


def main(folder, ndocs=400, nqueries=200, seed=30):
    rng = random.Random(seed)
    words = vocabulary(rng)
    weights = [1 / r for r in range(1, len(words) + 1)]
    out = Path(folder)
    out.mkdir(exist_ok=True)
    counts = Counter()
    for doc in range(ndocs):
        text, tokens = document(rng, words, weights, doc)
        (out / f"doc{doc:03}.txt").write_text(text, encoding="utf8")
        counts.update(t.lower() for t in tokens)
    (out / "README.md").write_text("Not a text of the corpus: not indexed.\n")
    with open(Path(folder).parent / "queries.txt", "w") as f:
        for _ in range(nqueries):
            k = rng.choice([1, 1, 2, 2, 3])
            f.write(" ".join(rng.choice(words[10:1500]) for _ in range(k)) + "\n")
    return counts


if __name__ == "__main__":
    counts = main(sys.argv[1] if len(sys.argv) > 1 else "corpus")
    print(f"{sum(counts.values())} words, {len(counts)} distinct, in 400 files")
    print("rank  word      count  rank x count")
    for r, (w, c) in enumerate(counts.most_common(), start=1):
        if r in (1, 2, 3, 10, 100, 1000):
            print(f"{r:4}  {w:8} {c:6}  {r * c:12}")
