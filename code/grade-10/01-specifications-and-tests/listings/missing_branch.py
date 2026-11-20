def grade(mark):
    """Return "fail", "pass" or "merit" for a mark from 0 to 20."""
    if mark < 10:
        return "fail"
    elif mark < 15:
        return "pass"
    elif mark > 15:
        return "merit"


for mark in [8, 12, 15, 17]:
    print(mark, grade(mark))
