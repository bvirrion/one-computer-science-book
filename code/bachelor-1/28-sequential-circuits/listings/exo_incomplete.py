"""exo_incomplete.py: a traffic light for a crossing, as a Moore machine; input 1 means
a pedestrian has pressed the button. Something is missing."""

DELTA = {("green", 0): "green", ("green", 1): "amber",
         ("amber", 0): "red", ("amber", 1): "red",
         ("red", 0): "green"}
SHOWS = {"green": "cars go", "amber": "cars slow", "red": "people cross"}


def run(word, state="green"):
    shown = []
    for button in word:
        state = DELTA[state, button]
        shown.append(SHOWS[state])
    return shown


if __name__ == "__main__":
    print(run([0, 1, 0, 0, 0]))
    try:
        print(run([1, 0, 1, 0]))
    except KeyError as e:
        print("KeyError:", e)
