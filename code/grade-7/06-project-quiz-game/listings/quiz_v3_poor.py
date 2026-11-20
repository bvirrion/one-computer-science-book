from questions import EASY_ANSWERS, EASY_QUESTIONS
from quiz_v3 import play

score = play(EASY_QUESTIONS, EASY_ANSWERS)
print("Your score:", score, "out of", len(EASY_QUESTIONS))
