from pathlib import Path

text = "Lighthouse Café\ncrêpes, 4 \u20ac\n"
Path("menu.txt").write_text(text, encoding="cp1252")

old = Path("menu.txt").read_text(encoding="cp1252")
Path("menu-utf8.txt").write_text(old, encoding="utf-8")

for name in ("menu.txt", "menu-utf8.txt"):
    print(name, Path(name).stat().st_size, "bytes")
print(Path("menu.txt").read_bytes()[-4:].hex(" "))
print(Path("menu-utf8.txt").read_bytes()[-6:].hex(" "))
# capture: scratch
