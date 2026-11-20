from pgm import pgm_text

image = []
for _ in range(4):
    row = []
    for c in range(6):
        row.append(c * 51)           # from black (0) to white (255), left to right
    image.append(row)
print(pgm_text(image))
