shopping = ["bread", "milk"]
print(shopping)
shopping.append("apples")       # add at the end
print(shopping)
shopping.insert(0, "eggs")      # add at index 0
print(shopping)
shopping.remove("milk")         # remove the first "milk"
print(shopping)
last = shopping.pop()           # remove the last item and give it back
print(last, shopping)
shopping[0] = "six eggs"        # replace the item at index 0
print(shopping)
