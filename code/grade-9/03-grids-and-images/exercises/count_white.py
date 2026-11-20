def count_white(image):
    """The number of pixels at 255."""
    count = 0
    for row in image:
        count = count + row.count(255)
    return count
