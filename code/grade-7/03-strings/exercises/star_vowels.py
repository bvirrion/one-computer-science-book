text = "Once upon a time"
starred = ""
for ch in text:
    if ch.lower() in "aeiou":
        starred = starred + "*"
    else:
        starred = starred + ch
print(starred)
