def letter_counts(text):
    """A dictionary: each letter of text and the number of times it appears."""
    counts = {}
    for letter in text.lower():
        if "a" <= letter <= "z":
            counts[letter] = counts.get(letter, 0) + 1
    return counts


def by_frequency(counts):
    """The letters, from the most frequent to the least."""
    return sorted(counts, key=lambda letter: -counts[letter])


if __name__ == "__main__":
    with open("passage.txt", encoding="utf-8") as f:
        passage = f.read()
    counts = letter_counts(passage)
    total = sum(counts.values())
    print(total, "letters")
    for letter in by_frequency(counts)[:10]:
        print(f"{letter}: {counts[letter]:>4}  {100 * counts[letter] / total:5.1f} %")
