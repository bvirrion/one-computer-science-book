from packets import cut

packets = cut("A fox in the garden at dusk!", 6, "192.0.2.15", "203.0.113.40")
arrived = [packets[3], packets[0], packets[4], packets[2]]       # number 1 is lost

pieces = {}
for packet in arrived:
    pieces[packet["number"]] = packet["data"]
message = ""
for number in range(len(packets)):
    message = message + pieces.get(number, "______")     # a hole for a lost piece
print(message)
