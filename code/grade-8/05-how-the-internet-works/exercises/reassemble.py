def reassemble(packets, count):
    """Rebuild a message from packets that may come twice; list the missing numbers."""
    pieces = {}
    for packet in packets:
        pieces[packet["number"]] = packet["data"]    # a copy replaces the same piece
    message = ""
    missing = []
    for number in range(count):
        if number in pieces:
            message = message + pieces[number]
        else:
            missing.append(number)
    return message, missing
