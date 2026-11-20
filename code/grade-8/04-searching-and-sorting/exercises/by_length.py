def sort_by_length(words):
    """Selection sort, comparing the lengths of the words."""
    for start in range(len(words) - 1):
        shortest = start
        for i in range(start + 1, len(words)):
            if len(words[i]) < len(words[shortest]):
                shortest = i
        words[start], words[shortest] = words[shortest], words[start]


words = ["banana", "fig", "cherry", "kiwi", "apple"]
sort_by_length(words)
print(words)
