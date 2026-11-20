from keyword_cipher import keyword_encrypt

with open("passage.txt", encoding="utf-8") as f:
    letters = ""
    for letter in f.read().lower():
        if "a" <= letter <= "z":
            letters = letters + letter
secret = keyword_encrypt(letters, "lamp")

first_seen = {}
distances = []
for k in range(len(secret) - 2):
    group = secret[k:k + 3]
    if group in first_seen:
        distances.append(k - first_seen[group])
    first_seen[group] = k
print(len(distances), "repeats; the first ten distances:", distances[:10])
for length in range(2, 9):
    divides = 0
    for d in distances:
        if d % length == 0:
            divides = divides + 1
    print(f"length {length}: divides {divides} distances")
