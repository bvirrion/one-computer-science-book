from gcd import gcd

record = 0
for a in range(1, 1000):
    for b in range(1, a):
        steps = gcd(a, b)[1]
        if steps > record:
            record = steps
            print(f"{a:>4} {b:>4}: {steps:>2} steps")
