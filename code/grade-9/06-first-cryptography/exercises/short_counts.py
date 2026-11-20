from frequencies import by_frequency, letter_counts

with open("passage.txt", encoding="utf-8") as f:
    letters = ""
    for letter in f.read().lower():
        if "a" <= letter <= "z":
            letters = letters + letter
for length in [20, 100, 1000]:
    counts = letter_counts(letters[:length])
    top = by_frequency(counts)[:5]
    print(length, "letters:", [letter + " " + str(counts[letter]) for letter in top])
