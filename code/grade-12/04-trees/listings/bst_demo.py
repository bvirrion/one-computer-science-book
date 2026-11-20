import csv

from bst import build, search
from node import height, size
from traversals import inorder

with open("books.csv", newline="") as f:
    titles = [row["title"] for row in csv.DictReader(f)]

t = build(titles[:10])                       # the first ten, in the table's order
print("root:", t.value, "| size", size(t), "| height", height(t))
print("left of root:", t.left.value, "| right of root:", t.right.value)
for title in ["The Lost Forest", "Seven Code", "The Lost Code"]:
    print(f"{title!r}: visited {search(t, title)}")
for title in inorder(t)[:4]:
    print("  ", title)
print("   ...", len(inorder(t)), "titles in alphabetical order")
