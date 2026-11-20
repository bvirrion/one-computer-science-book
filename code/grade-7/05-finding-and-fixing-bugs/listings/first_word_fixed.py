def first_word(sentence):
    end = sentence.find(" ")
    if end == -1:            # no space: the sentence is one word
        return sentence
    return sentence[:end]


for sentence in ["The fox ran", "Hello there", "Stop", "a"]:
    print("[" + first_word(sentence) + "]")
