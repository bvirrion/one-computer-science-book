def shift_letter(letter, key):
    return chr(ord(letter) + key)


print(shift_letter("a", 3), shift_letter("x", 3), shift_letter("z", 3))
