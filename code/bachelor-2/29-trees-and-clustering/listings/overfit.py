"""overfit.py: trees of growing depth on loans whose labels are 15 % noise; accuracy
on the training set and on a test set the tree never saw."""
from dataset import loans
from id3 import accuracy, id3

train, test = loans(700, seed=1, noise=0.15), loans(300, seed=2, noise=0.15)
print("depth  leaves  train   test")
for d in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]:
    tree = id3(train, max_depth=d)
    leaves = str(tree).count("'leaf'")
    print(f"{d:5} {leaves:7} {accuracy(tree, train):6.3f} {accuracy(tree, test):6.3f}")
