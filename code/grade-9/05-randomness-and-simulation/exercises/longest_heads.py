import random

random.seed(9)
longest = 0
run = 0
for _ in range(100):
    if random.choice(["heads", "tails"]) == "heads":
        run = run + 1
        if run > longest:
            longest = run
    else:
        run = 0
print("longest run of heads in 100 tosses:", longest)
