questions = [
    "What is the capital of France?",
    "How many legs does a spider have?",
    "What is 7 x 8?",
    "Which planet is the largest?",
    "What do bees make?",
    "How many minutes are in an hour?",
    "What is the opposite of hot?",
    "How many sides does a hexagon have?",
    "Which colour do blue and yellow make?",
    "What is 100 - 37?",
]
answers = ["paris", "8", "56", "jupiter", "honey",
           "60", "cold", "6", "green", "63"]

if len(questions) != len(answers):
    print("Error:", len(questions), "questions but", len(answers), "answers")
for i in range(len(questions)):
    print(i + 1, questions[i], "->", answers[i])
