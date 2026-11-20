"""Exercise 10: Chandy-Lamport when channels may reorder messages. Unrepaired, a
transfer sent after its sender recorded can overtake the marker and be counted twice.
Repaired, every transfer carries the snapshots its sender has recorded; a receiver that
sees a snapshot it has not recorded records before applying the money, and a channel
is closed only when all the transfers sent before the sender recorded have arrived
(the marker says how many)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from snapshot import TOTAL, Bank, Branch  # noqa: E402


class Repaired(Branch):
    def __init__(self, name, bank):
        super().__init__(name, bank)
        self.sent_to, self.got_from = {}, {}  # money messages per channel

    def send(self, dst, msg):
        if msg[0] == "money":
            self.sent_to[dst] = self.sent_to.get(dst, 0) + 1
            msg = ("money", msg[1], frozenset(self.snaps))
        super().send(dst, msg)

    def record(self, sid):
        self.snaps[sid] = {
            "balance": self.balance,
            "open": set(self.others()),
            "channels": 0,
            "expect": {},
            "seen": dict(self.got_from),
        }
        for p in self.others():  # the marker says how many transfers went before it
            super().send(p, ("marker", (sid, self.sent_to.get(p, 0))))

    def on_message(self, src, msg):
        if msg[0] == "money":
            _, amount, tags = msg
            for sid in sorted(tags - set(self.snaps)):
                self.record(sid)
            self.balance += amount
            self.got_from[src] = self.got_from.get(src, 0) + 1
            for sid, s in self.snaps.items():
                if src in s["open"] and sid not in tags:  # sent before src recorded
                    s["channels"] += amount
                    s["seen"][src] = s["seen"].get(src, 0) + 1
                    self.close(s, src)
        elif msg[0] == "marker":
            sid, count = msg[1]
            if sid not in self.snaps:
                self.record(sid)
            self.snaps[sid]["expect"][src] = count
            self.close(self.snaps[sid], src)
        else:
            super().on_message(src, msg)

    def close(self, s, src):
        if s["expect"].get(src) == s["seen"].get(src, 0):
            s["open"].discard(src)


def run(seed, repaired):
    bank = Bank(seed, Repaired if repaired else Branch, fifo=False)
    cl, _ = bank.run()
    still_open = sum(bool(b.snaps[s]["open"]) for b in bank.branches for s in b.snaps)
    return sum(t != TOTAL for t in cl), still_open


if __name__ == "__main__":
    for repaired in (False, True):
        wrong, still_open = run(25, repaired)
        print(
            f"repaired={repaired}: {wrong} of 100 snapshots wrong, "
            f"{still_open} channels never closed"
        )
