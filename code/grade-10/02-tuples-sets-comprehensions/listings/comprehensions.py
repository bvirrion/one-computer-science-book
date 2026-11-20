numbers = [4, 7, 10, 3, 8]

squares = [n * n for n in numbers]
evens = [n for n in numbers if n % 2 == 0]
print(squares)
print(evens)

words = ["map", "graph", "path", "grid", "maze"]
first_letters = {w[0] for w in words}
lengths = {w: len(w) for w in words}
print(sorted(first_letters))
print(lengths)

pairs = [(r, c) for r in range(2) for c in range(3)]
print(pairs)
