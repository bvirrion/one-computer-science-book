week = [0.0, 0.0, 0.7, 0.0, 6.9, 0.0, 0.3]
backwards = []
for amount in week:
    backwards.insert(0, amount)     # each new value goes in front
print(backwards)
