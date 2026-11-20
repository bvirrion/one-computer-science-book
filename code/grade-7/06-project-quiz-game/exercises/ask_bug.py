def normalise(text):
    return text.strip().lower()


def ask(question, answer):
    points = 0
    if normalise(input(question + " ")) == answer:
        points = 1
    if normalise(input("Try again: ")) == answer:
        points = points + 0.5
    return points
