# capture: scratch
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Buy milk\n")
    f.write("Return the library book\n")

with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line)

with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip(), "has", len(line), "characters")
