"""exo_autocomplete.py: the k first completions, without listing all of them."""
from text_gen import rows
from trie import Trie


def first_k(trie, prefix, k):
    """At most k words starting with prefix, in alphabetical order; stops early."""
    node, out, visited = trie.find(prefix), [], 0
    stack = [(node, prefix)] if node else []
    while stack and len(out) < k:
        node, word = stack.pop()
        visited += 1
        if node.end:
            out.append(word)
        for c in sorted(node.children, reverse=True):
            stack.append((node.children[c], word + c))
    return out, visited


titles = Trie()
for b in rows("books"):
    titles.insert(b["title"])
for prefix, k in [("The", 3), ("The S", 2), ("S", 4), ("Under", 5)]:
    words, visited = first_k(titles, prefix, k)
    print(f"{prefix!r} k={k}: {visited} nodes visited of {titles.find(prefix).size()}")
    print("   ", "; ".join(words))
