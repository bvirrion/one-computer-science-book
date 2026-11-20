keys = 1
for choices in range(26, 0, -1):     # 26 choices for a, then 25 for b, ...
    keys = keys * choices
print(f"{keys:,} substitution keys")
