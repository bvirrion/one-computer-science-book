from html_tree import name_of, tags

with open("first_page.html", encoding="utf-8") as f:
    page = f.read()

counts = {}
for tag in tags(page):
    if not tag.startswith("/") and not tag.startswith("!"):
        name = name_of(tag)
        counts[name] = counts.get(name, 0) + 1
for name in counts:
    print(name, counts[name])
print("elements:", sum(counts.values()))
