sentence = "the fox saw the hen and the hen saw the fox"
counts = {}
for word in sentence.split():
    counts[word] = counts.get(word, 0) + 1
    print(word, counts)
