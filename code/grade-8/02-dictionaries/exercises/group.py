def group_by_first_letter(words):
    groups = {}
    for word in words:
        first = word[0]
        if first not in groups:
            groups[first] = []
        groups[first].append(word)
    return groups


print(group_by_first_letter(["apple", "bean", "avocado", "cherry", "banana"]))
