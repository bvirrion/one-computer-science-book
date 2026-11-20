sentence = "A list holds many values in order."
spaces = 0
for ch in sentence:
    if ch == " ":
        spaces = spaces + 1
print(spaces, sentence.count(" "))
