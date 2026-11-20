"""The weekend problem: is greedy change right with the coins of Brenmoor?"""
from change_exhaustive import fewest
from change_greedy import greedy_change

BRENMOOR = [1, 2, 5, 12, 25, 40]


def failures(coins, upto):
    return [a for a in range(1, upto + 1)
            if len(greedy_change(a, coins)) > fewest(a, coins)[0]]


bad = failures(BRENMOOR, 100)
a = bad[0]
print("smallest failure:", a, "greedy", greedy_change(a, BRENMOOR),
      "fewest", fewest(a, BRENMOOR)[0])
print(len(bad), "failures up to 100:", bad)
print("fewest coins tried for 100:", fewest(100, BRENMOOR)[1], "combinations")
# Part IV: change one coin (not the 1) and check below the two largest added
for i in range(1, len(BRENMOOR)):
    for new in range(2, 50):
        coins = sorted(set(BRENMOOR[:i] + [new] + BRENMOOR[i + 1:]))
        if len(coins) == len(BRENMOOR) and not failures(coins, coins[-1] + coins[-2]):
            print(f"replace {BRENMOOR[i]} by {new}: {coins} never fails")
