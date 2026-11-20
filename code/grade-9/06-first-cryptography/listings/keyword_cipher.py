from shift import ALPHABET, shift_letter


def keyword_encrypt(text, keyword):
    """Shift each letter by the next letter of the keyword (a = 0, b = 1, ...)."""
    result = ""
    k = 0
    for letter in text.lower():
        if letter in ALPHABET:
            key = ALPHABET.index(keyword[k % len(keyword)])
            result = result + shift_letter(letter, key)
            k = k + 1
        else:
            result = result + letter
    return result


if __name__ == "__main__":
    print(keyword_encrypt("meet me at the lighthouse at nine", "lamp"))
