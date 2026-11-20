def most_frequent(sentence):
    counts = {}
    for word in sentence.split():
        counts[word] = counts.get(word, 0) + 1
    best = ""
    for word in counts:
        if best == "" or counts[word] > counts[best]:
            best = word
    return best


print(most_frequent("the fox saw the hen and the hen saw the fox"))
