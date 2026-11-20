"""hol_blocking.py: when four pages arrive, if one packet of the first is lost."""
ONE_WAY, PACKETS, PAGES = 25, 8, 4               # ms one way, packets per page, pages


def deliver(packets, lost, per_stream):
    """packets: (page, send time) in sending order; return when each page is complete.
    The lost packet is resent when the acks of the three after it have come back."""
    arrive = [t + ONE_WAY for _, t in packets]
    if lost is not None:
        arrive[lost] = packets[lost + 3][1] + 3 * ONE_WAY
    done, last = {}, {}
    for i, (page, _) in enumerate(packets):
        key = page if per_stream else "all"      # QUIC: per stream; TCP: one stream
        last[key] = max(arrive[i], last.get(key, 0))   # in order within the stream
        done[page] = last[key]
    return done


def interleaved():                               # HTTP/2 and /3: all pages at once
    return [(i % PAGES, ONE_WAY + i) for i in range(PAGES * PACKETS)]


def one_at_a_time(lost):                         # HTTP/1.1, one connection, in turn
    t, done = 0, {}
    for page in range(PAGES):
        packets = [(page, t + ONE_WAY + j) for j in range(PACKETS)]  # request, then
        done[page] = t = deliver(packets, lost if page == 0 else None, False)[page]
    return done


LOST = 4                                         # the 5th packet sent: page 0's
h1, h2 = one_at_a_time(LOST), deliver(interleaved(), LOST, False)
h3, clean = deliver(interleaved(), LOST, True), deliver(interleaved(), None, True)
print("page  HTTP/1.1  HTTP/2 (TCP)  HTTP/3 (QUIC)  no loss   (ms, page complete)")
for p in range(PAGES):
    print(f"{p:4} {h1[p]:9} {h2[p]:13} {h3[p]:14} {clean[p]:8}")
