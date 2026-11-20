def cut(text, size):
    """Cut text into numbered pieces of at most size characters."""
    pieces = []
    for start in range(0, len(text), size):
        pieces.append({"number": len(pieces), "data": text[start:start + size]})
    return pieces


for piece in cut("Meet me at the lighthouse at six.", 10):
    print(piece)
