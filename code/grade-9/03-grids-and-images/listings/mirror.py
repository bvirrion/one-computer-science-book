from pgm import pgm_text, read_pgm

image = read_pgm("shape.pgm")
for r in range(len(image)):
    image[r] = image[r][::-1]          # each row read backwards
print(pgm_text(image))
