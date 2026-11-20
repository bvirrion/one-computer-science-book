from frequencies import by_frequency, letter_counts
from keyword_cipher import keyword_encrypt
from shift import encrypt

with open("passage.txt", encoding="utf-8") as f:
    passage = f.read()
texts = [["plain", passage],
         ["shift 3", encrypt(passage, 3)],
         ["keyword lamp", keyword_encrypt(passage, "lamp")],
         ["keyword lighthouse", keyword_encrypt(passage, "lighthouse")]]
for name, text in texts:
    counts = letter_counts(text)
    total = sum(counts.values())
    top = by_frequency(counts)[:4]
    shares = ""
    for letter in top:
        shares = shares + f"  {letter} {100 * counts[letter] / total:4.1f} %"
    print(f"{name:<19}{shares}")
