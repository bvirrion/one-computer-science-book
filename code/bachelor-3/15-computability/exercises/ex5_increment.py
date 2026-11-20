"""ex5_increment.py -- exercise 5: a binary increment that fails on 111, and its fix."""
from tm import BLANK as B

BUGGY = {
    ("q0", "0"): ("q0", "0", "R"), ("q0", "1"): ("q0", "1", "R"),
    ("q0", B): ("carry", B, "L"),
    ("carry", "1"): ("carry", "0", "L"),
    ("carry", "0"): ("done", "1", "S"),
}

# The fix: a carry that runs off the left end must write a new leading 1.
FIXED = {**BUGGY, ("carry", B): ("done", "1", "S")}
