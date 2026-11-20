def rebuild(packets):
    pieces = {}
    for packet in packets:
        pieces[str(packet["number"])] = packet["data"]
    message = ""
    for number in sorted(pieces):
        message = message + pieces[number]
    return message
