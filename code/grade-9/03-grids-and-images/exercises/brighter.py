def brighter(image, amount):
    """Add amount to every grey level, kept between 0 and 255."""
    new = []
    for row in image:
        new_row = []
        for value in row:
            value = value + amount
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            new_row.append(value)
        new.append(new_row)
    return new
