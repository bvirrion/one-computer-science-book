from gates import NOR


def settle(s, r, q, qbar, steps=4):
    """Update both NOR gates at once, again and again, until nothing changes."""
    seen = [(q, qbar)]
    for _ in range(steps):
        q, qbar = NOR(r, qbar), NOR(s, q)
        if (q, qbar) == seen[-1]:
            return seen, True  # stable: the latch holds this state
        seen.append((q, qbar))
    return seen, False


q, qbar = 0, 1
for s, r, what in [(1, 0, "set"), (0, 0, "hold"), (0, 1, "reset"), (0, 0, "hold"),
                   (1, 1, "both"), (0, 0, "release")]:
    seen, stable = settle(s, r, q, qbar)
    q, qbar = seen[-1]
    end = f"Q={q}" if stable else "never settles"
    print(f"S={s} R={r} {what:8} {seen}  ->  {end}")
