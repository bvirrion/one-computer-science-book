"""The alternating-bit protocol over two lossy channels (data one way, acks back)."""
from lossy_channel import Channel


def run(messages, data_line, ack_line):
    sent_bit, expected, delivered, sends = 0, 0, [], 0
    for m in messages:
        while True:  # send m until its acknowledgement comes back
            sends += 1
            print(f"send ({sent_bit}, {m})", end="  ")
            frame = data_line.carry((sent_bit, m))
            if frame is None:
                print("lost; timeout")
                continue
            bit, data = frame
            if bit == expected:
                delivered.append(data)
                expected = 1 - expected
                print("delivered", end="  ")
            else:
                print("duplicate dropped", end="  ")
            ack = ack_line.carry(bit)   # the receiver acknowledges every frame
            if ack is None:
                print("ack lost; timeout")
                continue
            print(f"ack {ack}")
            if ack == sent_bit:
                sent_bit = 1 - sent_bit
                break
    return delivered, sends


if __name__ == "__main__":
    got, sends = run(["a", "b", "c", "d"], Channel(0.3, seed=10), Channel(0.3, seed=3))
    print("received", got, "after", sends, "sends")
