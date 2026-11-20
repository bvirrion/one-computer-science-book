# Every way to play 10 questions: a right first answers, b right second ones.
reachable = []
for a in range(11):
    for b in range(11 - a):
        score = a + 0.5 * b
        if score not in reachable:
            reachable.append(score)
print(len(reachable), "scores, from", min(reachable), "to", max(reachable))
