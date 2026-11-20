from shift import ALPHABET, shift_letter


def keyword_decrypt(text, keyword):
    """Undo the keyword cipher: shift each letter back by the keyword's letter."""
    result = ""
    k = 0
    for letter in text.lower():
        if letter in ALPHABET:
            key = ALPHABET.index(keyword[k % len(keyword)])
            result = result + shift_letter(letter, -key)
            k = k + 1
        else:
            result = result + letter
    return result


print(keyword_decrypt("xeqi xe mi ehq atgtisoghp af ctnq", "lamp"))
