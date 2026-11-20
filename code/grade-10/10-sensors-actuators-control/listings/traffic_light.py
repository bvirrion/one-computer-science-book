# A pedestrian crossing: the cars' light, and a button for pedestrians.
TABLE = {
    ("green", "tick"): "green",          # cars keep going
    ("green", "button"): "green wait",   # a pedestrian asked
    ("green wait", "tick"): "amber",
    ("green wait", "button"): "green wait",
    ("amber", "tick"): "red",
    ("amber", "button"): "amber",
    ("red", "tick"): "green",            # pedestrians crossed
    ("red", "button"): "red",
}
CARS_MAY_GO = {"green", "green wait", "amber"}

state = "green"
for event in ["tick", "button", "button", "tick", "tick", "tick", "tick"]:
    new = TABLE[(state, event)]
    cars = "go" if new in CARS_MAY_GO else "stop"
    print(f"{state:10} --{event:6}--> {new:10} cars {cars}")
    state = new
