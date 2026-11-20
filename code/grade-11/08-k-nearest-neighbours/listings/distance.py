import math


def distance(a, b):
    """Euclidean distance between two items (thickness, mass, ...); labels ignored."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


if __name__ == "__main__":
    letter, packet, parcel = (3.0, 50, "?"), (20.0, 300, "?"), (45.0, 320, "?")
    print("letter-packet:", distance(letter, packet))
    print("packet-parcel:", distance(packet, parcel))
