import random

random.seed(1)
throws = []
for _ in range(20):
    throws.append(random.randint(1, 6))
print("one die:  ", throws)

sums = []
for _ in range(10):
    sums.append(random.randint(1, 6) + random.randint(1, 6))
print("two dice: ", sums)

bag = ["red", "red", "red", "blue", "green"]
print("from the bag:", random.choice(bag), random.choice(bag), random.choice(bag))
