def exact(size):
    """The chance that two of size pupils share a birthday (365 days)."""
    all_different = 1
    for k in range(size):
        all_different = all_different * (365 - k) / 365
    return 1 - all_different


for size in [5, 10, 15, 20, 23, 25, 30, 40, 50, 60]:
    print(f"{size:>2} pupils: {exact(size):.3f}")
size = 1
while exact(size) <= 0.5:
    size = size + 1
print("smallest class above one half:", size, f"({exact(size):.4f})")
