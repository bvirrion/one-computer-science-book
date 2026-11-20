# Does (pupils + 49) // 50 always give "divide by 50, then round up"?
import math

wrong = 0
for pupils in range(1, 201):
    if (pupils + 49) // 50 != math.ceil(pupils / 50):
        wrong = wrong + 1
print("values that disagree:", wrong)
