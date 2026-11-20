"""exo_aho.py: a multi-pattern matcher: a trie of the patterns with failure links."""
from collections import deque

from text_gen import archive


def build(patterns):
    goto, fail, out = [{}], [0], [[]]  # node 0 is the root
    for p in patterns:
        v = 0
        for c in p:
            if c not in goto[v]:
                goto.append({})
                fail.append(0)
                out.append([])
                goto[v][c] = len(goto) - 1
            v = goto[v][c]
        out[v].append(p)
    queue = deque(goto[0].values())  # breadth first: shorter words first
    while queue:
        v = queue.popleft()
        for c, w in goto[v].items():
            f = fail[v]
            while f and c not in goto[f]:
                f = fail[f]
            fail[w] = goto[f][c] if c in goto[f] and goto[f][c] != w else 0
            out[w] += out[fail[w]]  # what ends at the longest border ends here too
            queue.append(w)
    return goto, fail, out


def search(text, patterns):
    goto, fail, out = build(patterns)
    v, found = 0, []
    for i, c in enumerate(text):
        while v and c not in goto[v]:
            v = fail[v]
        v = goto[v].get(c, 0)
        found += [(i - len(p) + 1, p) for p in out[v]]
    return found


patterns = ["he", "she", "his", "hers"]
print(search("ushers", patterns))
text = archive()
words = ["Forest", "Valley", "Riverside", "Hilltop", "Seven", "returned", "rain"]
found = search(text, words)
for w in words:
    assert sum(1 for _, p in found if p == w) == text.count(w)
print(len(found), "occurrences of", len(words), "words in one pass, as str.count finds")
