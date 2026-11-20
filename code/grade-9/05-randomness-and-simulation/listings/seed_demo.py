import random

random.seed(2026)
print([random.randint(1, 6) for _ in range(10)])
random.seed(2026)                        # the same seed again
print([random.randint(1, 6) for _ in range(10)])
random.seed(7)                           # another seed
print([random.randint(1, 6) for _ in range(10)])
print(random.random())
