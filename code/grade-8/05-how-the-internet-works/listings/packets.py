def cut(message, size, source, destination):
    """Cut a message into packets of at most size characters, each with a header."""
    packets = []
    number = 0
    for start in range(0, len(message), size):
        packets.append({"from": source, "to": destination, "number": number,
                        "data": message[start:start + size]})
        number = number + 1
    return packets


def rebuild(packets):
    """Put the pieces back in the order of their numbers."""
    pieces = {}
    for packet in packets:
        pieces[packet["number"]] = packet["data"]
    message = ""
    for number in range(len(pieces)):
        message = message + pieces[number]
    return message


if __name__ == "__main__":
    packets = cut("A fox in the garden at dusk!", 6, "192.0.2.15", "203.0.113.40")
    first = packets[0]
    print(len(packets), "packets; from", first["from"], "to", first["to"])
    arrived = [packets[3], packets[0], packets[4], packets[1], packets[2]]
    for packet in arrived:
        print(packet["number"], repr(packet["data"]))
    print(rebuild(arrived))
