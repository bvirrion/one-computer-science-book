stock = {"apples": 12, "pears": 5}
stock["plums"] = 20            # a new key: a new entry
stock["apples"] = 9            # a key already there: its value changes
del stock["pears"]
print(stock)
for fruit in stock:
    print(fruit, stock[fruit])
for fruit, count in stock.items():
    print(fruit, "->", count)
