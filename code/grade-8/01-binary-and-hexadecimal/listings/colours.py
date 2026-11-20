def rgb(code):
    """The three numbers of a colour written #RRGGBB."""
    red = int(code[1:3], 16)
    green = int(code[3:5], 16)
    blue = int(code[5:7], 16)
    return [red, green, blue]


for code in ["#FF8800", "#2E8B57", "#4169E1"]:
    print(code, rgb(code))
