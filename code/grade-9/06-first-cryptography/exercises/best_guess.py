from shift import encrypt

COMMON = ["the", "and", "a", "to", "of", "in", "at", "is", "it", "on"]


def score(text):
    """How many words of text are common English words."""
    points = 0
    for word in text.split():
        if word in COMMON:
            points = points + 1
    return points


def best_decryption(ciphertext):
    best = ""
    for key in range(1, 26):
        candidate = encrypt(ciphertext, -key)
        if score(candidate) > score(best):
            best = candidate
    return best


print(best_decryption("vjg mggrgt nkv vjg ncor cv vjg gpf qh vjg fca"))
