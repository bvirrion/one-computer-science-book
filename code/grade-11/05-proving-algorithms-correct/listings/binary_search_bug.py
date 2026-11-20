def search(t, x, cap=50):
    lo, hi = 0, len(t)
    turns = 0
    while lo < hi:
        turns = turns + 1
        if turns > cap:   # a guard for this demonstration only
            raise RuntimeError(f"no end after {cap} turns: lo={lo}, hi={hi}")
        mid = (lo + hi) // 2
        if t[mid] == x:
            return mid
        if t[mid] < x:
            lo = mid      # the bug: mid was already compared
        else:
            hi = mid
    return None


t = [3, 8, 12, 15, 21, 30, 34, 41, 47, 52]
for x in t:
    assert search(t, x) == t.index(x)
print("all", len(t), "tests pass")
try:
    print(search(t, 20))
except RuntimeError as error:
    print("RuntimeError:", error)
