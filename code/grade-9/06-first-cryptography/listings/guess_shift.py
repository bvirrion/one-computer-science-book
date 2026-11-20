from frequencies import by_frequency, letter_counts
from shift import encrypt


def guess_key(ciphertext):
    """Guess a shift key: the most frequent letter is taken to be an e."""
    top = by_frequency(letter_counts(ciphertext))[0]
    return (ord(top) - ord("e")) % 26


if __name__ == "__main__":
    with open("passage.txt", encoding="utf-8") as f:
        message = f.read().split("\n\n")[1]
    secret = encrypt(message, 11)
    print(secret.split("\n")[0])
    key = guess_key(secret)
    print("guessed key:", key)
    print(encrypt(secret, -key).split("\n")[0])
    print("whole message right:", encrypt(secret, -key) == message.lower())
