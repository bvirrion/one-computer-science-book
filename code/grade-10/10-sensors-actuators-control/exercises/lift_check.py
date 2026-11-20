"""Problem: the reachable states of the lift, checked; and the waits of some calls."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from lift import safe, step  # noqa: E402

EVENTS = ["call0", "call1", "call2", "open", "close", "arrive"]
START = (0, "closed", "stop", None)


def reachable(start=START, step=step):
    """All the states reachable from start: try every event in every state found."""
    found = {start}
    to_visit = [start]
    while to_visit:
        state = to_visit.pop()
        for event in EVENTS:
            new = step(state, event)
            if new not in found:
                found.add(new)
                to_visit.append(new)
    return found


def serve(calls, start=START):
    """Serve the calls one after the other; return the events needed for each."""
    state, waits = start, []
    for k in calls:
        events = 0
        if state[1] == "open":
            state, events = step(state, "close"), events + 1
        state, events = step(state, f"call{k}"), events + 1
        while state[2] != "stop":
            state, events = step(state, "arrive"), events + 1
        waits.append(events)
    return waits


if __name__ == "__main__":
    states = reachable()
    print(len(states), "reachable states")
    print("unsafe:", [s for s in states if not safe(s)])
    print("door open:", sorted(s for s in states if s[1] == "open"))
    waits = serve([2, 0, 1, 2, 1])
    print("events per call:", waits, " mean", sum(waits) / len(waits))
