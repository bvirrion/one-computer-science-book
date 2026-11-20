"""exo_gbn_ack.py: a receiver that acknowledges what it received (exercise 6)."""
from go_back_n import Receiver, transfer


class WrongReceiver(Receiver):
    def on_packet(self, packet):
        seq, item = packet
        if seq == self.expected % self.M:
            self.out.append(item)
            self.expected += 1
            self.done = self.clock.now
        self.link.send(seq)                      # the bug: ack it, in order or not


data = list(range(1000))
out, t, link = transfer(data, k=4, window=15, loss=0.05, seed=2, receiver=WrongReceiver)
print(f"delivered {len(out)} of {len(data)}; intact {out == data}")
missing = sorted(set(data) - set(out))
print("first missing packets:", missing[:5])
