"""budget.py: the time of a first visit and of a revisit, in round trips."""
RTT, RESOLVER, UPSTREAM = 80, 10, 40             # ms: to the server, to our resolver,
                                                 # from the resolver to name servers


def visit(lookup_misses, cached_name=False, open_connection=False):
    lookup = 0 if cached_name else RESOLVER + lookup_misses * UPSTREAM
    connect = 0 if open_connection else 2 * RTT  # TCP handshake, then TLS 1.3's
    return lookup + connect + RTT                # and the request itself


for label, ms in (("first visit, resolver knows nothing", visit(3)),
                  ("first visit, resolver knows brenmoor.test", visit(1)),
                  ("first visit, resolver has the name", visit(0)),
                  ("revisit, name cached on the machine", visit(0, cached_name=True)),
                  ("revisit, connection still open", visit(0, True, True))):
    print(f"{label:42} {ms:4} ms")
