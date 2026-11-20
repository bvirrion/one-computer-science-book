import random


def rle_encode(s):
    """Return the list of (count, character) runs of the string s."""
    runs = []
    for ch in s:
        if runs and runs[-1][1] == ch:
            runs[-1] = (runs[-1][0] + 1, ch)
        else:
            runs.append((1, ch))
    return runs


def rle_decode(runs):
    return "".join(ch * count for count, ch in runs)


row = "WWWWWWWWWWBBBWWWWWWWWWWWWWWWWBBBBBBBBWWWWWWWWWWWWWWWWWW"
runs = rle_encode(row)
print(runs)
print(rle_decode(runs) == row, len(row), "characters,", len(runs), "runs")

rng = random.Random(7)
noise = "".join(rng.choice("WB") for _ in range(len(row)))
print(noise)
print(len(rle_encode(noise)), "runs for", len(noise), "characters")
