from pgm import pgm_text, read_pgm

image = read_pgm("shape.pgm")
for r in range(len(image)):
    for c in range(len(image[r])):
        if image[r][c] >= 128:
            image[r][c] = 255
        else:
            image[r][c] = 0
print(pgm_text(image))
