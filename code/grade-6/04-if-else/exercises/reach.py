t = int(input("Temperature: "))
if t < 0:
    print("ice")
elif t < 20:
    print("cool")
elif t <= 30:
    print("warm")
else:
    print("hot")
