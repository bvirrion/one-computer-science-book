from html_tree import show_tree

page = """<body>
  <p>Open every day <em>except Monday.</p>
  <h2>This week</h2>
  <p>Chess club on Saturday.</p>
</body>"""
print("open at the end:", show_tree(page))
