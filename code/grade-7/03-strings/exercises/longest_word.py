def longest_word(sentence):
    words = sentence.split()
    best = words[0]
    for word in words:
        if len(word) > len(best):
            best = word
    return best


print(longest_word("the quick brown fox jumps over the lazy dog"))
