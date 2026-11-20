name = "Lighthouse Café"
data = name.encode("utf-8")
print(data.hex(" "))
wrong = data.decode("latin-1")
print(len(name), len(wrong), ascii(wrong))
print(wrong.encode("latin-1").decode("utf-8"))
