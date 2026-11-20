def is_binary(text):
    """True when text is not empty and every character is 0 or 1."""
    if len(text) == 0:
        return False
    for ch in text:
        if ch != "0" and ch != "1":
            return False
    return True


for text in ["1101", "102", ""]:
    if is_binary(text):
        print(text, "->", int(text, 2))
    else:
        print(text, "is not a binary number")
