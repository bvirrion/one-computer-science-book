data = "Café".encode("latin-1")
print(data)
print(data.decode("utf-8", errors="backslashreplace"))
print(data.decode("utf-8"))
# capture: exit
