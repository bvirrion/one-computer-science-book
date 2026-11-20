def area(width, length):
    return width * length


kitchen = area(3, 4)
print("Kitchen:", kitchen)
print("Bedroom:", area(3.5, 4))
print("Both:", kitchen + area(3.5, 4))
