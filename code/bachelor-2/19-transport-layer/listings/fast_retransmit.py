"""fast_retransmit.py: go-back-N resends at the third duplicate ack (exercise 9)."""
import go_back_n
from go_back_n import transfer


class FastSender(go_back_n.Sender):
    def __init__(self, *args):
        super().__init__(*args)
        self.dups = 0

    def on_ack(self, seq):
        if (seq - self.base) % self.M == self.M - 1 and self.base < self.next:
            self.dups += 1                       # an ack for base - 1: a duplicate
            if self.dups == 3:                   # three: base is surely lost
                self.next = self.base            # go back now, not at the timeout
                self.arm()
                self.fill()
            return
        self.dups = 0
        super().on_ack(seq)


data = list(range(5000))
for name, sender in (("timeout only", go_back_n.Sender),
                     ("fast retransmit", FastSender)):
    out, t, link = transfer(data, k=6, window=31, timeout=300, loss=0.02, seed=11,
                            sender=sender)
    print(f"{name:16} intact {out == data}  {link.sent} sent  {t / 1000:.1f} s")
