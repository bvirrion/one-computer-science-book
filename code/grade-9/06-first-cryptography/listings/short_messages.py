import random

from guess_shift import guess_key
from shift import encrypt

with open("passage.txt", encoding="utf-8") as f:
    letters = ""
    for letter in f.read().lower():
        if "a" <= letter <= "z":
            letters = letters + letter

random.seed(9)
for length in [10, 20, 50, 100, 200, 500, 1000]:
    right = 0
    for _ in range(100):
        start = random.randint(0, len(letters) - length)
        message = letters[start:start + length]
        key = random.randint(1, 25)
        if guess_key(encrypt(message, key)) == key:
            right = right + 1
    print(f"{length:>4} letters: key found {right:>3} times out of 100")
