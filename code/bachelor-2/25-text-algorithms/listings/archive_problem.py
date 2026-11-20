"""archive_problem.py: the town archive: searched, its names completed, compressed."""
from kmp import kmp
from lzw import encode
from naive import naive
from text_gen import archive, rows
from trie import Trie

text = archive()
pattern = "returned Under the"
(f1, c1), (f2, c2) = naive(text, pattern), kmp(text, pattern)
print(f"I-II  {pattern!r}: {len(f1)} occurrences; naive {c1}, KMP {c2} comparisons")

people = {p["person_id"]: f"{p['first_name']} {p['last_name']}" for p in rows("people")}
names = sorted({people[m["person_id"]] for m in rows("members")})
t = Trie()
for name in names:
    t.insert(name)
letters = sum(map(len, names))
print(f"III   {len(names)} borrowers' names, {letters} letters, {t.size()} trie nodes")
for prefix in ["Wen", "Gr", "Leo B"]:
    print(f"      {prefix!r}: {t.words(prefix)}")

print("IV    LZW on a^n: n, codes =", ", ".join(f"{n}:{len(encode(b'a' * n))}"
                                            for n in [1, 3, 6, 10, 55, 5050, 5051]))
data = text.encode()
for size in [1000, 4000, 16000, 64000, len(data)]:
    codes = len(encode(data[:size]))
    print(f"      first {size:5} bytes: {codes:5} codes, {size / codes:4.1f} a code")
