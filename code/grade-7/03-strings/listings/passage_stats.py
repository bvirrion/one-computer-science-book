passage = """The fox looked at the hen, and the hen looked at the fox.
Neither of them moved. Then the farmer's dog barked, and both ran."""

letters = 0
for ch in passage:
    if ch.isalpha():
        letters = letters + 1
words = passage.split()
print("characters:", len(passage))
print("letters:", letters)
print("words:", len(words))

lower = passage.lower()
for letter in "aeiou":
    print(letter, lower.count(letter))
