speed = 300_000 * 2 / 3            # light in a glass fibre: about 200,000 km per second

for km in [10, 1_000, 20_000]:
    seconds = km / speed
    print(f"{km:>6} km: {seconds * 1000:.2f} ms")

photo_bits = 3_000_000 * 8         # a photo of 3 megabytes
rate = 10_000_000                  # 10 megabits per second
print("sending the photo:", photo_bits / rate, "s")
