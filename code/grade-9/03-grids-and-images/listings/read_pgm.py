from pgm import read_pgm

image = read_pgm("shape.pgm")
print(len(image[0]), "x", len(image), "pixels")
print("top left:", image[0][0], " arrow tip:", image[6][14])
print("row 6:", image[6])
