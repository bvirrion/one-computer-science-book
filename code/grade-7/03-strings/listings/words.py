sentence = "the fox and the hen and the dog"
words = sentence.split(" ")
print(words)
print(len(words), "words")
print(words.count("the"), "times the")
print("-".join(words))
