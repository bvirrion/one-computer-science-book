"""sr_too_wide.py: selective repeat with k = 2 and W = 3, one more than allowed."""
from selective_repeat import Receiver


class Log:
    def send(self, seq):
        print(f"  receiver acks {seq}")


r = Receiver(k=2, window=3)
r.link, r.clock = Log(), type("Clock", (), {"now": 0.0})()
print("the sender sends packets 0, 1, 2 with sequence numbers 0, 1, 2")
for i in range(3):
    r.on_packet((i, f"packet {i}"))
print("all three acks are lost; the sender times out and resends packet 0 (sequence 0)")
r.on_packet((0, "packet 0"))
print("the receiver keeps it as packet 4:", r.buffer)
print("later the real packet 3 arrives")
r.on_packet((3, "packet 3"))
print("the receiver delivered:", r.out)
