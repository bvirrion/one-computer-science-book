"""trie_demo.py: the town's street names in a trie; autocompletion."""
from text_gen import street_names
from trie import Trie, compressed

names = street_names()
t = Trie()
for name in names:
    t.insert(name)
letters = sum(len(name) for name in names)
print(f"{len(names)} names, {letters} letters, {t.size()} nodes")
for prefix in ["Mill", "Ch", "S", "River Lane", "Riv", "Bridge Road ", "Z"]:
    print(f"{prefix!r:14} -> {t.words(prefix)}")
print("'Mill Row' in the trie:", "Mill Row" in t, "  'Mill' in the trie:", "Mill" in t)

eight = Trie()
for name in ["Castle Road", "Castle Row", "Castle Way", "Market Road", "Market Row",
             "Mill Avenue", "Mill Row", "Mill Street"]:
    eight.insert(name)
print(f"eight names: {eight.size()} nodes; compressed (* = a name ends):")
print("\n".join(compressed(eight)))
