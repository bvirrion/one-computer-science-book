"""exo_lcrs.py: exercise 3."""

from lcrs import Tree, show, to_binary

print(show(to_binary(Tree(1, [Tree(2, [Tree(4)]), Tree(3)]))))
print(show(to_binary(Tree(1, [Tree(2), Tree(3), Tree(4)]))))
