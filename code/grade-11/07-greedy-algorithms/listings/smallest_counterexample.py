"""Systems of three coins 1 < a < b <= 8 where greedy change can go wrong."""
from change_exhaustive import fewest
from change_greedy import greedy_change

for b in range(3, 9):
    for a in range(2, b):
        coins = [1, a, b]
        bad = [m for m in range(1, a + b)          # below the two largest added
               if len(greedy_change(m, coins)) > fewest(m, coins)[0]]
        if bad:
            m = bad[0]
            print(f"coins {coins}: first failure at {m}:",
                  f"greedy {greedy_change(m, coins)}, fewest {fewest(m, coins)[0]}")
