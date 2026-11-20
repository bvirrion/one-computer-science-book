photo = 3_000_000                  # bytes
packet = 1_500                     # bytes in a packet, header included
header = 40                        # bytes of header in each packet
data = packet - header             # bytes of the photo in each packet

packets = photo // data
if photo % data != 0:
    packets = packets + 1          # one more packet for the end of the photo
total = photo + packets * header
print(packets, "packets,", packets * header, "bytes of headers,", total, "bytes in all")

speed = 300_000 / 1.468            # km per second in a glass fibre
propagation = 20_000 / speed
print(f"propagation over 20,000 km: {propagation:.3f} s")

for rate in [10_000_000, 100_000_000, 1_000_000_000]:
    sending = total * 8 / rate
    print(f"{rate // 1_000_000:>5} Mbit/s: sending {sending:.3f} s,"
          f" in all {sending + propagation:.3f} s")
