def shift_letter(letter, key):
    """Move a letter key places, keeping capitals; leave other characters."""
    if "a" <= letter <= "z":
        return chr((ord(letter) - ord("a") + key) % 26 + ord("a"))
    if "A" <= letter <= "Z":
        return chr((ord(letter) - ord("A") + key) % 26 + ord("A"))
    return letter


def encrypt(text, key):
    result = ""
    for letter in text:
        result = result + shift_letter(letter, key)
    return result


print(encrypt("Meet Me at Noon, by the Zoo!", 3))
