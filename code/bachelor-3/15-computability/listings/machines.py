"""machines.py -- three Turing machines run on the simulator, with traces."""
from tm import BLANK as B
from tm import accepts, run

INCREMENT = {  # binary + 1: go to the last digit, then carry leftwards
    ("q0", "0"): ("q0", "0", "R"), ("q0", "1"): ("q0", "1", "R"),
    ("q0", B): ("carry", B, "L"),
    ("carry", "1"): ("carry", "0", "L"),  # 1 + carry = 0, carry on
    ("carry", "0"): ("done", "1", "S"), ("carry", B): ("done", "1", "S"),
}

PALINDROME = {  # cross off the first letter, check the last one matches, repeat
    ("q0", "a"): ("has_a", B, "R"), ("q0", "b"): ("has_b", B, "R"),
    ("q0", B): ("accept", B, "S"),
    ("has_a", "a"): ("has_a", "a", "R"), ("has_a", "b"): ("has_a", "b", "R"),
    ("has_a", B): ("end_a", B, "L"),
    ("has_b", "a"): ("has_b", "a", "R"), ("has_b", "b"): ("has_b", "b", "R"),
    ("has_b", B): ("end_b", B, "L"),
    ("end_a", "a"): ("back", B, "L"), ("end_a", B): ("accept", B, "S"),
    ("end_b", "b"): ("back", B, "L"), ("end_b", B): ("accept", B, "S"),
    ("back", "a"): ("back", "a", "L"), ("back", "b"): ("back", "b", "L"),
    ("back", B): ("q0", B, "R"),
}

ADD = {  # unary addition: 111+11 becomes 11111
    ("q0", "1"): ("q0", "1", "R"), ("q0", "+"): ("q0", "1", "R"),
    ("q0", B): ("last", B, "L"),
    ("last", "1"): ("done", B, "S"),  # one 1 too many: erase it
}

if __name__ == "__main__":
    run(INCREMENT, "1011", trace=print)
    for w in ("0", "111", "1001"):
        print(f"increment {w}: {run(INCREMENT, w)[2]}")
    for w in ("abba", "aba", "abab", ""):
        print(f"palindrome {w!r}: {accepts(PALINDROME, w)}, steps "
              f"{run(PALINDROME, w)[3]}")
    print("add 111+11:", run(ADD, "111+11")[2])
