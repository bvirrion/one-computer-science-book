def rotate(image):
    """The image turned a quarter turn clockwise."""
    height = len(image)
    new = []
    for c in range(len(image[0])):
        row = []
        for r in range(height):
            row.append(image[height - 1 - r][c])
        new.append(row)
    return new
