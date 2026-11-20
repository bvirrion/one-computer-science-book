from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from binary_search import binary_search  # noqa: E402

numbers = list(range(1, 1001))
most = 0
for target in numbers:
    position, guesses = binary_search(numbers, target)
    if guesses > most:
        most = guesses
print("at most", most, "guesses for 1 to 1000")
