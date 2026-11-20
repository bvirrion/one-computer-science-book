text = "Once upon a time, a fox lived in a quiet wood."
vowels = 0
for ch in text:
    if ch in "aeiouAEIOU":
        vowels = vowels + 1
print("vowels:", vowels)

no_spaces = ""
for ch in text:
    if ch != " ":
        no_spaces = no_spaces + ch
print(no_spaces)
