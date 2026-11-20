"""ex6_anbn.py -- exercise 6: a Turing machine that accepts exactly the words a^n b^n
(n >= 0). It crosses off one a (as X) and one b (as Y) per round."""
from tm import BLANK as B

ANBN = {
    ("q0", "a"): ("find_b", "X", "R"),  # cross off the leftmost a
    ("q0", "Y"): ("check", "Y", "R"),  # no a left: only Ys may remain
    ("q0", B): ("accept", B, "S"),  # the empty word
    ("find_b", "a"): ("find_b", "a", "R"),
    ("find_b", "Y"): ("find_b", "Y", "R"),
    ("find_b", "b"): ("back", "Y", "L"),  # cross off the matching b
    ("back", "a"): ("back", "a", "L"),
    ("back", "Y"): ("back", "Y", "L"),
    ("back", "X"): ("q0", "X", "R"),  # just right of the last X
    ("check", "Y"): ("check", "Y", "R"),
    ("check", B): ("accept", B, "S"),
}
