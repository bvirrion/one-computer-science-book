def normalise(text):
    return text.strip().lower()


def ask(question, answer):
    """Like quiz_v4's ask, but "skip" moves on at once with 0 points."""
    typed = normalise(input(question + " "))
    if typed == "skip":
        print("Skipped.")
        return 0
    if typed == answer:
        print("Right!")
        return 1
    if normalise(input("Not quite. Try again: ")) == answer:
        print("Right, half a point.")
        return 0.5
    print("The answer was", answer + ".")
    return 0
