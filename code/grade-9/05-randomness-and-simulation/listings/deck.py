import random

random.seed(5)
deck = []
for suit in ["spades", "hearts", "diamonds", "clubs"]:
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
        deck.append(rank + " " + suit)
print(len(deck), "cards; the first three:", deck[:3])
random.shuffle(deck)
hand = deck[:5]
print("a hand of five:", hand)
print(len(deck[5:]), "cards left")
