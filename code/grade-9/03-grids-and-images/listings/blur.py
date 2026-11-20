from pgm import pgm_text, read_pgm


def blur(image):
    """Each pixel becomes the average of itself and its neighbours, rounded."""
    new = []
    for r in range(len(image)):
        row = []
        for c in range(len(image[0])):
            total = 0
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < len(image) and 0 <= c + dc < len(image[0]):
                        total = total + image[r + dr][c + dc]
                        count = count + 1
            row.append(round(total / count))
        new.append(row)
    return new


if __name__ == "__main__":
    print(pgm_text(blur(read_pgm("shape.pgm"))))
