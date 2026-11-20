def normalise(text):
    """The typed answer without spaces at the ends, in small letters."""
    return text.strip().lower()


def ask(question, answer):
    """Ask one question; return 1 point for a right answer, 0 otherwise."""
    typed = input(question + " ")
    if normalise(typed) == answer:
        print("Right!")
        return 1
    print("The answer was", answer + ".")
    return 0


if __name__ == "__main__":
    points = ask("What is the capital of France?", "paris")
    print("points:", points)
