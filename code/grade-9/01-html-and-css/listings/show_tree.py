from html_tree import show_tree

with open("first_page.html", encoding="utf-8") as f:
    page = f.read()
left_open = show_tree(page)
print("open at the end:", left_open)
