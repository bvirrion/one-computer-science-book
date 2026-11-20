"""Stop and wait: the sender is busy for T, then idle for one round trip."""

PACKET = 1500 * 8  # bits


def utilisation(rate, rtt):
    t = PACKET / rate              # time to put the packet on the line
    return t / (t + rtt)


for name, rate, rtt in [("one room", 100e6, 0.0002), ("one town", 100e6, 0.002),
                        ("one country", 1e9, 0.02), ("faster line", 10e9, 0.02)]:
    u = utilisation(rate, rtt)
    print(f"{name:12} {rate / 1e6:>6.0f} Mbit/s  rtt {rtt * 1000:>4} ms  "
          f"busy {u:7.3%}  useful {u * rate / 1e6:6.2f} Mbit/s")
