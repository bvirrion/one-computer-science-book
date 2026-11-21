def cut(text, size):
    """Cut text into pieces numbered from 1, each one knowing how many there are."""
    total = (len(text) + size - 1) // size
    pieces = []
    for start in range(0, len(text), size):
        data = text[start:start + size]
        pieces.append({"number": len(pieces) + 1, "of": total, "data": data})
    return pieces


for piece in cut("Meet me at the lighthouse at six.", 10):
    print(piece)
