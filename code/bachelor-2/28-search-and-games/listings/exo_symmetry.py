"""exo_symmetry.py: noughts and crosses positions counted, then counted again up to the
eight symmetries of the square."""
from tictactoe import moves

ROT = [6, 3, 0, 7, 4, 1, 8, 5, 2]  # quarter turn: new cell i holds old cell ROT[i]
FLIP = [2, 1, 0, 5, 4, 3, 8, 7, 6]  # mirror left-right


def images(b):
    out = []
    for _ in range(4):
        b = "".join(b[i] for i in ROT)
        out += [b, "".join(b[i] for i in FLIP)]
    return out


def canonical(b):
    return min(images(b))


seen, canon, todo = {"." * 9}, {"." * 9}, ["." * 9]
while todo:
    b = todo.pop()
    for m in moves(b):
        if m not in seen:
            seen.add(m)
            canon.add(canonical(m))
            todo.append(m)
print(f"positions reachable: {len(seen)}; up to symmetry: {len(canon)}")
