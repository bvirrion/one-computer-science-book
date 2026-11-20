french = {"the": "le", "cat": "chat", "eats": "mange", "fish": "poisson"}
sentence = "the cat eats the mouse"
words = []
for word in sentence.split():
    words.append(french.get(word, word))      # unknown words stay as they are
print(" ".join(words))
