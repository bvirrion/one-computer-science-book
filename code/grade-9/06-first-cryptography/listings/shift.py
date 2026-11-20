ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def shift_letter(letter, key):
    """The letter moved key places round the alphabet; other characters stay."""
    if letter not in ALPHABET:
        return letter
    return chr((ord(letter) - ord("a") + key) % 26 + ord("a"))


def encrypt(text, key):
    """The shift cipher: every letter of text moved key places."""
    result = ""
    for letter in text.lower():
        result = result + shift_letter(letter, key)
    return result


if __name__ == "__main__":
    print(encrypt("meet me at the lighthouse at nine", 3))
    print(encrypt("xyz", 3))
