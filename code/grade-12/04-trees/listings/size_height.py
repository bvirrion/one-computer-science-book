from node import Node, height, leaves, size

#        A
#      /   \
#     B     C
#    / \     \
#   D   E     F
#      /
#     G
t = Node("A", Node("B", Node("D"), Node("E", Node("G"))), Node("C", None, Node("F")))
print("size", size(t), "| height", height(t), "| leaves", leaves(t))
print("subtree B: size", size(t.left), "| height", height(t.left))
print("single node: height", height(Node("X")), "| empty tree: height", height(None))
