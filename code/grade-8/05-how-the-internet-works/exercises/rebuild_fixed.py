def rebuild(packets):
    pieces = {}
    for packet in packets:
        pieces[packet["number"]] = packet["data"]       # numbers stay numbers
    message = ""
    for number in sorted(pieces):
        message = message + pieces[number]
    return message
