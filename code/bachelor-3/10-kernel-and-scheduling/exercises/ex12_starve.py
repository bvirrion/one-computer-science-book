"""ex12_starve.py -- shortest remaining time first starves a long job under a stream of
short ones; aging, which counts each unit waited against the work left, bounds its
wait."""


def stream(n):  # one long job, then a short job every 2 units
    return [("long", 0, 20)] + [(f"s{k}", 1 + 2 * k, 2) for k in range(n)]


def srtf(jobs, age=None):
    """Unit by unit; the key is the work left, minus waited/age with aging.
    Returns name -> finish time."""
    left = {name: burst for name, _, burst in jobs}
    arrival = {name: a for name, a, _ in jobs}
    ran = {name: 0 for name, _, _ in jobs}  # units of CPU received so far
    finish, t = {}, 0
    while len(finish) < len(jobs):
        ready = [n for n in left if arrival[n] <= t and n not in finish]
        if not ready:
            t += 1
            continue

        def key(n, t=t):
            waited = t - arrival[n] - ran[n]
            return (left[n] - (waited / age if age else 0), arrival[n])

        n = min(ready, key=key)
        left[n] -= 1
        ran[n] += 1
        t += 1
        if left[n] == 0:
            finish[n] = t
    return finish
