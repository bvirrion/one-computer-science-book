import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def random_key(seed):
    """A mixed alphabet: the letter that replaces a, then b, and so on."""
    random.seed(seed)
    letters = list(ALPHABET)
    random.shuffle(letters)
    return "".join(letters)


def substitute(text, source, target):
    """Replace each letter of source found in text by the letter of target."""
    result = ""
    for letter in text.lower():
        if letter in source:
            result = result + target[source.index(letter)]
        else:
            result = result + letter
    return result


if __name__ == "__main__":
    key = random_key(2026)
    print("plain: ", ALPHABET)
    print("key:   ", key)
    secret = substitute("meet me at the lighthouse at nine", ALPHABET, key)
    print(secret)
    print(substitute(secret, key, ALPHABET))      # the same table, read upwards
