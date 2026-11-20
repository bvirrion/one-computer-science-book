from questions import EASY_ANSWERS, EASY_QUESTIONS
from quiz_v2 import ask


def play(questions, answers):
    """Ask every question in order; return the score."""
    score = 0
    for i in range(len(questions)):
        score = score + ask(questions[i], answers[i])
    return score


if __name__ == "__main__":
    score = play(EASY_QUESTIONS, EASY_ANSWERS)
    print("Your score:", score, "out of", len(EASY_QUESTIONS))
    if score == len(EASY_QUESTIONS):
        print("A perfect game!")
