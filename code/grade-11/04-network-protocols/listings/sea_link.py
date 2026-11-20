"""The weekend problem: a window of w packets on a cable under the sea."""
import math

RATE = 1e9               # bit/s
PACKET = 1500 * 8        # bits
DISTANCE = 6000e3        # m
SPEED = 2e8              # m/s, the speed of the signal in the cable

t = PACKET / RATE                    # sending one packet
rtt = 2 * DISTANCE / SPEED           # there and back; the ack's own time neglected
print(f"T = {t * 1e6:.0f} us, RTT = {rtt * 1e3:.0f} ms")
for w in [1, 10, 100, 1000, 5000, 5001]:
    u = min(1, w * t / (t + rtt))
    print(f"window {w:5}: busy {u:9.4%}, {u * RATE / 1e6:7.2f} Mbit/s")
print("smallest full window:", math.ceil((t + rtt) / t), "packets")
print(f"data in flight at full rate: {RATE * rtt / 8 / 1e6:.1f} MB")
