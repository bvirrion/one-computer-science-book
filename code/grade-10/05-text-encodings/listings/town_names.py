import town

names = [place["name"] for place in town.load("places")]
for encoding in ("utf-8", "utf-16-le", "latin-1"):
    total = sum(len(name.encode(encoding)) for name in names)
    print(f"{encoding:9}  {total} bytes for {len(names)} names")
print([name for name in names if not name.isascii()])
