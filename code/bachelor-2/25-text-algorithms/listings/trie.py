"""trie.py: a trie of words, with search and the words under a prefix."""


class Trie:
    def __init__(self):
        self.children = {}  # a letter -> the subtrie
        self.end = False  # a word ends here

    def insert(self, word):
        node = self
        for c in word:
            node = node.children.setdefault(c, Trie())
        node.end = True

    def find(self, prefix):
        """The node reached by reading prefix, or None."""
        node = self
        for c in prefix:
            node = node.children.get(c)
            if node is None:
                return None
        return node

    def __contains__(self, word):
        node = self.find(word)
        return node is not None and node.end

    def words(self, prefix=""):
        """The words that start with prefix, in alphabetical order."""
        node, out = self.find(prefix), []
        stack = [(node, prefix)] if node else []
        while stack:
            node, word = stack.pop()
            if node.end:
                out.append(word)
            for c in sorted(node.children, reverse=True):  # smallest letter on top
                stack.append((node.children[c], word + c))
        return out

    def size(self):
        return 1 + sum(child.size() for child in self.children.values())


def compressed(node, depth=0):
    """The lines of the compressed trie: each chain of single children is one edge."""
    lines = []
    for c in sorted(node.children):
        label, child = c, node.children[c]
        while len(child.children) == 1 and not child.end:
            (d, child), = child.children.items()
            label += d
        lines.append("    " * depth + repr(label) + (" *" if child.end else ""))
        lines += compressed(child, depth + 1)
    return lines
