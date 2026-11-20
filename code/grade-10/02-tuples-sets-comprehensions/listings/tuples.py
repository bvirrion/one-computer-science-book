point = (3, 4)
print(point, point[0], len(point))

x, y = point
print("x =", x, "y =", y)

a = 1
b = 2
a, b = b, a
print("a =", a, "b =", b)

single = (7,)
not_a_tuple = (7)
print(single, type(single), not_a_tuple, type(not_a_tuple))
