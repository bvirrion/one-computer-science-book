from naive import search_naive

n = 1000
text = "a" * n
for m in [2, 5, 10, 50, 100]:
    p = "a" * (m - 1) + "b"                 # matches m - 1 letters, then fails
    positions, comparisons = search_naive(text, p)
    print(f"m = {m:3}: {comparisons:6} comparisons = (n - m + 1) * m =",
          (n - m + 1) * m)
