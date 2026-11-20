"""confusion.py: the confusion matrix of the depth-2 tree on the noisy test set."""
from dataset import loans
from id3 import id3, predict

train, test = loans(700, seed=1, noise=0.15), loans(300, seed=2, noise=0.15)
tree = id3(train, max_depth=2)
m = [[0, 0], [0, 0]]  # m[true][predicted]
for x, y in test:
    m[y][predict(tree, x)] += 1
print("              predicted on time  predicted late")
print(f"on time       {m[0][0]:17} {m[0][1]:15}")
print(f"late          {m[1][0]:17} {m[1][1]:15}")
late = m[1][0] + m[1][1]
print(f"accuracy {(m[0][0] + m[1][1]) / len(test):.3f};",
      f"always 'on time' would score {(len(test) - late) / len(test):.3f}")
print(f"late loans caught: {m[1][1]} of {late}; false alarms: {m[0][1]}")
