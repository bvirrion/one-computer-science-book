"""encode_decode.py: a title through the catalogue's Huffman code and back."""

from collections import Counter

from huffman import catalogue, codewords, huffman_tree


def encode(text, code):
    return "".join(code[ch] for ch in text)


def decode(bits, tree):
    """Walk down the tree, one bit per step; at a leaf, output its symbol, restart."""
    out, node = [], tree
    for b in bits:
        node = node[int(b)]  # 0: left, 1: right
        if isinstance(node, str):
            out.append(node)
            node = tree
    assert node is tree, "the bits end inside a codeword"
    return "".join(out)


def main():
    text = catalogue()
    tree = huffman_tree(Counter(text))
    code = codewords(tree)
    title = text.split("\n")[0]
    bits = encode(title, code)
    print(f"{title!r}: {len(title)} characters, {len(bits)} bits")
    print(bits)
    print(repr(decode(bits, tree)))
    assert decode(encode(text, code), tree) == text
    print("whole catalogue: decoded back exactly")


if __name__ == "__main__":
    main()
