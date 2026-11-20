"""A channel that loses some of what it carries, at random but reproducibly."""
import random


class Channel:
    def __init__(self, loss, seed):
        self.loss = loss                  # the probability of losing each item
        self.rng = random.Random(seed)

    def carry(self, item):
        """Return the item, or None if it was lost on the way."""
        return None if self.rng.random() < self.loss else item
