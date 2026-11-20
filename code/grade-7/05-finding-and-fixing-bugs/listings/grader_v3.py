# grader_v3.py -- a letter and a comment for a quiz score from 0 to 99
WORDS = ["poor", "poor", "poor", "poor", "poor",
         "fair", "fair", "good", "good", "great"]


def letter(score):
    if score > 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "D"


def comment(score):
    tens = score // 10
    return WORDS[tens]


def grade(score):
    return letter(score) + " (" + comment(score) + ")"


if __name__ == "__main__":
    for score in [45, 50, 75, 90, 99]:
        print(score, grade(score))
