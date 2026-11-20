with open("books.csv", encoding="utf-8") as f:
    lines = f.readlines()
print(len(lines), "lines")
for line in lines[:4]:
    print(line.strip())
