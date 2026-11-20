from questions import EASY_ANSWERS, EASY_QUESTIONS, HARD_ANSWERS, HARD_QUESTIONS
from quiz_v2 import normalise


def ask(question, answer):
    """1 point for a right first answer, 0.5 for a right second one, else 0."""
    if normalise(input(question + " ")) == answer:
        print("Right!")
        return 1
    if normalise(input("Not quite. Try again: ")) == answer:
        print("Right, half a point.")
        return 0.5
    print("The answer was", answer + ".")
    return 0


def play(questions, answers):
    score = 0.0
    for i in range(len(questions)):
        score = score + ask(questions[i], answers[i])
    return score


def choose_level():
    """Return the level the player types: "easy" or "hard"."""
    level = normalise(input("Level (easy or hard)? "))
    while level != "easy" and level != "hard":
        level = normalise(input("Please type easy or hard: "))
    return level


if __name__ == "__main__":
    if choose_level() == "easy":
        questions = EASY_QUESTIONS
        answers = EASY_ANSWERS
    else:
        questions = HARD_QUESTIONS
        answers = HARD_ANSWERS
    score = play(questions, answers)
    print("Your score:", score, "out of", len(questions))
