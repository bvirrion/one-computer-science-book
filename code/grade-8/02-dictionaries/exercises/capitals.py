capitals = {"France": "Paris", "Italy": "Rome", "Japan": "Tokyo", "Kenya": "Nairobi"}


def capital(country):
    return capitals.get(country, "not known")


print(capital("Japan"), "/", capital("Peru"))
