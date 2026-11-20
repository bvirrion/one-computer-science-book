"""Invented items of the town's sorting office: thickness (mm), mass (g), class."""
import random

# class: (how many, mean thickness, spread, mean mass, spread)
KINDS = {"letter": (100, 4, 2, 60, 40),
         "packet": (130, 18, 8, 350, 180),
         "parcel": (70, 40, 15, 550, 250)}


def make_items(seed=2026):
    rng = random.Random(seed)
    items = []
    for label, (count, t, dt, m, dm) in KINDS.items():
        for _ in range(count):
            thickness = max(0.5, rng.gauss(t, dt))
            mass = max(5.0, rng.gauss(m, dm))
            items.append((round(thickness, 1), round(mass), label))
    rng.shuffle(items)
    return items


def split(items):
    """180 to learn from, 60 to choose k, 60 kept untouched until the end."""
    return items[:180], items[180:240], items[240:]
