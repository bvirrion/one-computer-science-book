"""The ballots of the weekend problem: 40 for 6 candidates, then 400 for 20."""

CANDIDATES = ["Ada", "Ben", "Chloe", "Dev", "Eva", "Femi"]
BALLOTS = [
    "Chloe", "Ada", "Eva", "Chloe", "Ben", "Dev", "Chloe", "Ada", "Femi", "Eva",
    "Chloe", "Dev", "Ada", "Chloe", "Eva", "Ben", "Ada", "Chloe", "Dev", "Eva",
    "Femi", "Chloe", "Ada", "Eva", "Chloe", "Ben", "Dev", "Ada", "Chloe", "Eva",
    "Ada", "Femi", "Chloe", "Eva", "Dev", "Ada", "Chloe", "Ben", "Eva", "Ada",
]


def many_ballots(count, candidates):
    """A longer, made-up election: ballot i goes to the candidate a fixed rule picks."""
    ballots = []
    for i in range(count):
        ballots.append(candidates[(i * i + 3 * i) % len(candidates)])
    return ballots
