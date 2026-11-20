from frequencies import by_frequency, letter_counts
from substitution import ALPHABET, random_key, substitute

with open("passage.txt", encoding="utf-8") as f:
    paragraphs = f.read().split("\n\n")
known = paragraphs[0] + paragraphs[1]          # a long text we can read
message = paragraphs[2] + paragraphs[3]        # the message to protect
secret = substitute(message, ALPHABET, random_key(7))

known_order = "".join(by_frequency(letter_counts(known)))
for letter in ALPHABET:                         # letters never seen go last
    if letter not in known_order:
        known_order = known_order + letter
secret_order = "".join(by_frequency(letter_counts(secret)))
print("known: ", known_order)
print("secret:", secret_order)


def show(guess):
    right = 0
    for k in range(len(guess)):
        if guess[k] == message.lower()[k] and guess[k] in ALPHABET:
            right = right + 1
    print(guess[:62], "...", right, "right")


guess = substitute(secret, secret_order, known_order)
show(guess)
guess = substitute(guess, "on", "no")          # "aod" must be "and"
show(guess)
guess = substitute(guess, "ro", "or")          # "trdab" looks like "today"
show(guess)
print("letters in the message:", sum(letter_counts(message).values()))
