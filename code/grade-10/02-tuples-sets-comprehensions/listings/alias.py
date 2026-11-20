a = [1, 2, 3]
b = a
b.append(4)
print("a:", a, " b:", b, " a is b:", a is b)

c = list(a)
c.append(5)
print("a:", a, " c:", c, " a is c:", a is c)
print("a == [1, 2, 3, 4]:", a == [1, 2, 3, 4])
