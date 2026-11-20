def mirror(word):
    """Reverse the word, then swap b and d, p and q, as in a mirror."""
    result = ""
    for ch in word[::-1]:
        i = "bdpq".find(ch)
        if i >= 0:
            ch = "dbqp"[i]
        result = result + ch
    return result


for word in ["bid", "bud", "pod", "pq", "box"]:
    print(word, mirror(word), mirror(word) == word)
