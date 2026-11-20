def first_word(sentence):
    end = sentence.find(" ")
    return sentence[:end]


for sentence in ["The fox ran", "Hello there", "Stop", "a"]:
    print("[" + first_word(sentence) + "]")
