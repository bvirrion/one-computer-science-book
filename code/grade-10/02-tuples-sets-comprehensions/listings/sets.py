genres_ana = set(["mystery", "sport", "history", "mystery"])
genres_ben = {"poetry", "sport", "science"}

print(genres_ana)
print(len(genres_ana), "sport" in genres_ana, "poetry" in genres_ana)
print("both:  ", genres_ana & genres_ben)
print("either:", genres_ana | genres_ben)
print("only Ana:", genres_ana - genres_ben)

seen = set()
for word in ["to", "be", "or", "not", "to", "be"]:
    seen.add(word)
print(len(seen), "different words")
