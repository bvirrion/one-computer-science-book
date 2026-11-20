from html_tree import VOID, name_of, tags


def stats(text):
    """The number of elements of an HTML text, and the depth of its tree."""
    count = 0
    depth = 0          # how many elements are open
    deepest = 0
    for tag in tags(text):
        if tag.startswith("!"):
            continue
        if tag.startswith("/"):
            depth = depth - 1
        else:
            count = count + 1
            if depth + 1 > deepest:
                deepest = depth + 1      # this element's level in the tree
            if name_of(tag) not in VOID:
                depth = depth + 1
    return count, deepest


def list_page(n):
    """A page whose body holds a heading and a list of n items."""
    items = ""
    for i in range(1, n + 1):
        items = items + "<li>item " + str(i) + "</li>"
    return ("<!DOCTYPE html><html><head><title>List</title></head><body>"
            "<h1>List</h1><ul>" + items + "</ul></body></html>")


for name in ["first_page.html", "table.html", "weather_page.html"]:
    with open(name, encoding="utf-8") as f:
        count, depth = stats(f.read())
    print(f"{name:<18} {count:>3} elements, depth {depth}")
for n in range(1, 11):
    count, depth = stats(list_page(n))
    print(f"list of {n:>2}: {count:>2} elements, depth {depth}")
