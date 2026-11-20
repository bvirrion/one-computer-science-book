def normalise(text):
    return text.strip().lower()


QUESTIONS = [
    "How many legs does a spider have?",
    "Which colour do blue and yellow make?",
]
ANSWERS = [["8", "eight"], ["green"]]


def ask(question, accepted):
    """1 point when the typed answer is any of the accepted ones."""
    if normalise(input(question + " ")) in accepted:
        print("Right!")
        return 1
    print("The answer was", accepted[0] + ".")
    return 0
