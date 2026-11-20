"""make_log.py: one day of the library's access log, made with a fixed seed."""

import random

ACTIONS = ["search"] * 5 + ["borrow"] * 3 + ["return"] * 3 + ["renew"]
REASONS = ["no-such-book", "limit-reached", "card-expired"]
HOURS = list(range(8, 20))
WEIGHTS = [2, 5, 9, 8, 4, 6, 5, 6, 9, 7, 3, 1]  # quiet at opening and closing


def make_log(seed=2025, n=640):
    rng = random.Random(seed)
    visitors = rng.sample(range(1, 61), 42)  # the members who come in that day
    times = sorted(
        (rng.choices(HOURS, WEIGHTS)[0], rng.randrange(60), rng.randrange(60))
        for _ in range(n)
    )
    lines = []
    for h, m, s in times:
        action = rng.choice(ACTIONS)
        anonymous = action == "search" and rng.random() < 0.4
        member = "-" if anonymous else str(rng.choice(visitors))
        book = rng.randint(1, 80)
        line = f"2025-11-14 {h:02d}:{m:02d}:{s:02d} member={member} action={action}"
        line += f" book={book}"
        if member != "-" and rng.random() < 0.06:
            line += f" status=error reason={rng.choice(REASONS)}"
        else:
            line += " status=ok"
        lines.append(line)
    return lines


if __name__ == "__main__":
    print("\n".join(make_log()))
