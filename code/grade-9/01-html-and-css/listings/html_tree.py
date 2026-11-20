VOID = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"]     # elements without an end tag


def tags(text):
    """The tags of an HTML text, in order, each without its angle brackets."""
    found = []
    start = text.find("<")
    while start != -1:
        end = text.find(">", start)
        found.append(text[start + 1:end])
        start = text.find("<", end)
    return found


def name_of(tag):
    """The element name of a tag: 'li class="new"' gives 'li', '/li' gives 'li'."""
    return tag.strip("/").split(" ")[0].lower()


def show_tree(text):
    """Print the element names, indented by their depth in the tree."""
    depth = 0
    for tag in tags(text):
        if tag.startswith("!"):
            continue                       # the DOCTYPE line is not an element
        if tag.startswith("/"):
            depth = depth - 1              # an end tag closes the open element
        else:
            print("  " * depth + name_of(tag))
            if name_of(tag) not in VOID:
                depth = depth + 1          # what follows is inside this element
    return depth
