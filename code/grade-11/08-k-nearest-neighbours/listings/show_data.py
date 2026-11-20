from collections import Counter

from parcels import make_items, split

items = make_items()
print(len(items), "items:", dict(Counter(label for _, _, label in items)))
for thickness, mass, label in items[:5]:
    print(f"  {thickness:5} mm {mass:5} g   {label}")
train, validation, test = split(items)
print("split:", len(train), "to learn,", len(validation), "to choose k,",
      len(test), "for the final test")
