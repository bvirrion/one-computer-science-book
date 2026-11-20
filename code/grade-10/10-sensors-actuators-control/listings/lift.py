def step(state, event):
    """The next state of the lift; an event that does not apply changes nothing."""
    floor, door, motor, target = state
    if event == "close" and door == "open":
        return (floor, "closed", motor, target)
    if event == "open" and motor == "stop":
        return (floor, "open", motor, target)
    if event.startswith("call") and door == "closed" and motor == "stop":
        k = int(event[4:])
        if k == floor:
            return (floor, "open", "stop", None)
        return (floor, "closed", "up" if k > floor else "down", k)
    if event == "arrive" and motor != "stop":
        floor += 1 if motor == "up" else -1
        if floor == target:
            return (floor, "open", "stop", None)   # stop first, then open
        return (floor, door, motor, target)
    return state


def safe(state):
    floor, door, motor, target = state
    return not (door == "open" and motor != "stop")


if __name__ == "__main__":
    state = (0, "open", "stop", None)
    events = ["call2", "close", "call2", "arrive", "open", "arrive", "close", "call0"]
    for event in events:
        state = step(state, event)
        print(f"{event:7} -> floor {state[0]}, door {state[1]:6}, motor {state[2]:4}"
              f"  safe: {safe(state)}")
