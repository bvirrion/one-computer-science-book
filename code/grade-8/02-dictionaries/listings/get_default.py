phone = {"Grandma": "0612 345 678", "Sami": "0698 765 432"}
for name in ["Sami", "Leo"]:
    print(name, phone.get(name, "not in the contacts"))
