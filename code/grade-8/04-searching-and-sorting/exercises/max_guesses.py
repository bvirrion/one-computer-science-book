from binary_search import binary_search

numbers = list(range(1, 1001))
most = 0
for target in numbers:
    position, guesses = binary_search(numbers, target)
    if guesses > most:
        most = guesses
print("at most", most, "guesses for 1 to 1000")
