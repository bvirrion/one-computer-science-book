"""exo_minimax.py: the minimax value of the tree of exercise 5, min to move first."""
from alphabeta import minimax

TREE = [[[4, 8, 2], [7, 1]], [[3], [9, 6], [5, 0]], [[6, 2], [1, 3, 8]]]
print("min at the root:", minimax(TREE, False, [0]),
      "| max at the root:", minimax(TREE, True, [0]))
