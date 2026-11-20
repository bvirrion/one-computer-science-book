"""sr_latch.py: two NOR gates feeding each other remember a bit; traced one time unit
(one gate delay) at a time, through set, hold, reset, and the forbidden input."""

from seq import Net


def sr_latch():
    n = Net("S", "R")
    n.gate("Q", "NOR", "R", "Qn")  # Qn is Q', the complement
    n.gate("Qn", "NOR", "S", "Q")
    return n


if __name__ == "__main__":
    n = sr_latch()
    v = {"S": 0, "R": 0, "Q": 0, "Qn": 1}
    print("phase      S R   Q Q' after each time unit")
    for name, s, r in [("set", 1, 0), ("hold", 0, 0), ("reset", 0, 1), ("hold", 0, 0),
                       ("forbidden", 1, 1), ("release", 0, 0)]:
        v |= {"S": s, "R": r}
        seen = []
        for _ in range(6):
            v = n.tick(v)
            seen.append(f"{v['Q']}{v['Qn']}")
        print(f"{name:10} {s} {r}   {' '.join(seen)}")
