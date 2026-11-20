import random

random.seed(12)
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = []
for rank in ranks:
    for _ in range(4):                 # four suits
        deck.append(rank)
draws = 100_000
pairs = 0
for _ in range(draws):
    random.shuffle(deck)
    if deck[0] == deck[1]:
        pairs = pairs + 1
print(f"simulated: {pairs / draws:.4f}   exact: 3/51 = {3 / 51:.4f}")
