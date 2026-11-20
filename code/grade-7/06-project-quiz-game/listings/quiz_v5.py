from questions import EASY_ANSWERS, EASY_QUESTIONS, HARD_ANSWERS, HARD_QUESTIONS
from quiz_v4 import choose_level, play


def result_line(level, score, total):
    """One line in a fixed format, easy to read for a person or a program."""
    return "RESULT level=" + level + " score=" + str(score) + "/" + str(total)


def main():
    level = choose_level()
    if level == "easy":
        questions = EASY_QUESTIONS
        answers = EASY_ANSWERS
    else:
        questions = HARD_QUESTIONS
        answers = HARD_ANSWERS
    score = play(questions, answers)
    print(result_line(level, score, len(questions)))


if __name__ == "__main__":
    main()
