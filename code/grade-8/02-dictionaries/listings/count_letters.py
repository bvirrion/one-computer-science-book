text = "the fox and the hen"
counts = {}
for ch in text:
    if ch != " ":
        counts[ch] = counts.get(ch, 0) + 1
print(counts)
print("e appears", counts["e"], "times")
