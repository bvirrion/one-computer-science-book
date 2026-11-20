import grader_v2
import grader_v3
import grader_v4


def expected(score):
    """The grade worked out another way: from the score's tens digit."""
    tens = score // 10
    words = ["poor"] * 5 + ["fair"] * 2 + ["good"] * 2 + ["great"]
    if score >= 90:
        letter = "A"
    elif score >= 75:
        letter = "B"
    elif score >= 50:
        letter = "C"
    else:
        letter = "D"
    return letter + " (" + words[tens] + ")"


for name, module in [("v2", grader_v2), ("v3", grader_v3), ("v4", grader_v4)]:
    wrong = []
    for score in range(100):
        if module.grade(score) != expected(score):
            wrong.append(score)
    print(name, len(wrong), "wrong answers out of 100, first ones:", wrong[:5])
