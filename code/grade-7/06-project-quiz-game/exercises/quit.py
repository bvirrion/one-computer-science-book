def normalise(text):
    return text.strip().lower()


def play(questions, answers):
    """Ask the questions in order until they run out or the player types quit."""
    score = 0
    i = 0
    playing = True
    while playing and i < len(questions):
        typed = normalise(input(questions[i] + " "))
        if typed == "quit":
            playing = False
        elif typed == answers[i]:
            score = score + 1
        i = i + 1
    return score
