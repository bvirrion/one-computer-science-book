names = {
    "library.brenmoor.example": "203.0.113.7",
    "weather.brenmoor.example": "203.0.113.12",
    "school.brenmoor.example": "198.51.100.30",
}


def look_up(name):
    """The address of a name, as the name system answers it, or None."""
    return names.get(name)


for name in ["weather.brenmoor.example", "pool.brenmoor.example"]:
    print(name, "->", look_up(name))
