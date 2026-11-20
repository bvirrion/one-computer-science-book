"""tcp_states.py: TCP's connection states, driven by events (no data, no timers)."""
MACHINE = {
    ("CLOSED", "open as server"): ("LISTEN", ""),
    ("CLOSED", "open as client"): ("SYN-SENT", "send SYN"),
    ("LISTEN", "receive SYN"): ("SYN-RECEIVED", "send SYN+ACK"),
    ("SYN-SENT", "receive SYN+ACK"): ("ESTABLISHED", "send ACK"),
    ("SYN-RECEIVED", "receive ACK"): ("ESTABLISHED", ""),
    ("ESTABLISHED", "close"): ("FIN-WAIT-1", "send FIN"),
    ("ESTABLISHED", "receive FIN"): ("CLOSE-WAIT", "send ACK"),
    ("FIN-WAIT-1", "receive ACK"): ("FIN-WAIT-2", ""),
    ("FIN-WAIT-1", "receive FIN"): ("CLOSING", "send ACK"),
    ("FIN-WAIT-2", "receive FIN"): ("TIME-WAIT", "send ACK"),
    ("CLOSING", "receive ACK"): ("TIME-WAIT", ""),
    ("CLOSE-WAIT", "close"): ("LAST-ACK", "send FIN"),
    ("LAST-ACK", "receive ACK"): ("CLOSED", ""),
    ("TIME-WAIT", "2 MSL pass"): ("CLOSED", ""),
}


def run(name, events, state="CLOSED"):
    for e in events:
        state, action = MACHINE[(state, e)]     # a missing pair is a protocol error
        print(f"{name:7} {e:16} -> {state:13} {action}".rstrip())
    return state


if __name__ == "__main__":
    run("client", ["open as client", "receive SYN+ACK"])
    run("server", ["open as server", "receive SYN", "receive ACK"])
    print("the client closes first:")
    run("client", ["close", "receive ACK", "receive FIN", "2 MSL pass"], "ESTABLISHED")
    run("server", ["receive FIN", "close", "receive ACK"], "ESTABLISHED")
