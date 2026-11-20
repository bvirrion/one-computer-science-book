"""exo_rk_multi.py: Rabin-Karp for several patterns of one length, in one pass."""
from text_gen import archive

BASE, Q = 256, 1_000_003


def rk_multi(text, patterns):
    m = len(patterns[0])
    assert all(len(p) == m for p in patterns)

    def h(word):
        v = 0
        for c in word:
            v = (v * BASE + ord(c)) % Q
        return v

    wanted = {}  # a hash value -> the patterns that have it
    for p in patterns:
        wanted.setdefault(h(p), []).append(p)
    high, hw = pow(BASE, m - 1, Q), h(text[:m])
    found = {p: [] for p in patterns}
    for s in range(len(text) - m + 1):
        for p in wanted.get(hw, []):
            if text[s:s + m] == p:
                found[p].append(s)
        if s < len(text) - m:
            hw = ((hw - ord(text[s]) * high) * BASE + ord(text[s + m])) % Q
    return found


text = archive()
found = rk_multi(text, ["Forest", "Valley", "Bridge", "Silent", "Garden", "Hidden"])
for p, where in found.items():
    assert len(where) == text.count(p)
    print(f"{p}: {len(where)}")
