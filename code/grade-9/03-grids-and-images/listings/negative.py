from pgm import pgm_text, read_pgm

image = read_pgm("shape.pgm")
for r in range(len(image)):
    for c in range(len(image[r])):
        image[r][c] = 255 - image[r][c]
print(pgm_text(image))
