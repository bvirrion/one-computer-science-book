"""exo_lzw_bug.py: a decoder that looks every code up in its table."""
from lzw import encode


def decode_short(codes):
    table = [bytes([b]) for b in range(256)]
    out, prev = [], None
    for code in codes:
        word = table[code]
        out.append(word)
        if prev is not None:
            table.append(prev + word[:1])
        prev = word
    return b"".join(out)


for text in [b"banana bandana", b"she sells sea shells", b"abababa"]:
    try:
        print(text, decode_short(encode(text)) == text)
    except IndexError as error:
        print(text, "IndexError:", error)
