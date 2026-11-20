"""Exercises 5, 6, 7, 10, 11 and 13: small controllers and their checks."""


def to_celsius(raw, low=-20.0, high=60.0, levels=1024):
    return low + raw * (high - low) / (levels - 1)


def next_state_buggy(table, state, event):
    return table[(state, event)]                   # KeyError on a missing pair


def next_state(table, state, event):
    return table.get((state, event), state)        # no transition: stay


def thermostat(t, heater, on_below=18.0, off_above=21.0):
    """Heater on below 18 degrees, off above 21, unchanged in between."""
    if t < on_below:
        return True
    if t > off_above:
        return False
    return heater


def switches(trace, controller, heater=False):
    count = 0
    for t in trace:
        new = controller(t, heater)
        count += new != heater
        heater = new
    return count


def lift_step_buggy(state, event):
    """A lift that accepts a call while its door is open."""
    floor, door, motor, target = state
    if event.startswith("call") and motor == "stop":
        k = int(event[4:])
        if k != floor:
            return (floor, door, "up" if k > floor else "down", k)
    return state


def check_safe(states, events, step, safe):
    """Return the (state, event) pairs that lead from a safe state to an unsafe one."""
    return [(s, e) for s in states for e in events if safe(s) and not safe(step(s, e))]


def barrier(state, event, capacity=3):
    """A car park barrier: state = (cars inside, barrier position)."""
    cars, position = state
    if event == "car at entry" and position == "down" and cars < capacity:
        return (cars + 1, "down")  # opened, the car passed, closed again
    if event == "car at exit" and cars > 0:
        return (cars - 1, position)
    return state
