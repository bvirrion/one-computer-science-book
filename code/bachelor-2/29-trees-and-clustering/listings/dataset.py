"""dataset.py: the chapter's generated data, the same at every run. Loans with five
features and a planted rule for lateness, points in the plane in planted clusters,
and the habits of the library's 60 members. Nothing is downloaded."""
import random

FEATURES = ["days", "pages", "age", "prior", "distance"]


def rule(x):
    """The planted rule: a loan comes back late when its member already returned two
    books late or more and lives at least 2,500 m from the library."""
    return int(x["prior"] >= 2 and x["distance"] >= 2500)


def loans(n, seed, noise=0.0):
    """n loans as (features, late); each label is flipped with probability noise."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        x = {"days": rng.choice([7, 14, 21, 28]),
             "pages": rng.randrange(80, 900),
             "age": rng.randrange(8, 86),
             "prior": rng.choices(range(7), weights=[40, 25, 15, 10, 5, 3, 2])[0],
             "distance": 10 * rng.randrange(20, 600)}
        y = rule(x)
        if rng.random() < noise:
            y = 1 - y
        out.append((x, y))
    return out


def blobs(seed=1, per=30, spread=0.7):
    """Points around five planted centres."""
    rng = random.Random(seed)
    centres = [(2, 2), (8, 3), (5, 8), (1, 9), (9, 9)]
    return [(round(rng.gauss(cx, spread), 2), round(rng.gauss(cy, spread), 2))
            for cx, cy in centres for _ in range(per)]


def small_points():
    """Twelve points in three loose groups, for clustering by hand."""
    return [(1.0, 1.0), (2.2, 1.4), (1.3, 2.9), (4.6, 1.6), (6.8, 1.1), (8.1, 2.2),
            (9.0, 0.9), (7.9, 3.9), (4.2, 6.8), (5.1, 8.9), (6.3, 7.6), (3.0, 8.7)]


def members(seed=4):
    """The 60 members' habits: loans a year and mean days kept, in three groups."""
    rng = random.Random(seed)
    groups = [(30, 9, 4, 2), (12, 24, 3, 3), (4, 12, 1.5, 3)]  # loans, days, spreads
    out = []
    for loans_mean, days_mean, s1, s2 in groups:
        for _ in range(20):
            out.append((max(1, round(rng.gauss(loans_mean, s1))),
                        max(3, round(rng.gauss(days_mean, s2)))))
    return out
