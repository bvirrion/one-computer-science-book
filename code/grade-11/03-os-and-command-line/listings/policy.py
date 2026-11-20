"""The smallest modes that meet the policy exactly: try all 512 for each file."""
from timetable import FILES, USERS, can

ALL, TEACHERS = "ana ben chloe dev", "ana ben"
POLICY = {  # path: {rights: the users who must have them; nobody else may}
    "/school": {"r": ALL, "w": "ana", "x": ALL},
    "/school/timetable.txt": {"r": ALL, "w": TEACHERS, "x": ""},
    "/school/news.txt": {"r": ALL, "w": "ben", "x": ""},
    "/school/marks": {"r": TEACHERS, "w": TEACHERS, "x": TEACHERS},
    "/school/marks/g11.csv": {"r": TEACHERS, "w": TEACHERS, "x": ""},
    "/school/exam.txt": {"r": "ben", "w": "ben", "x": ""},
}
RIGHT = {"r": 4, "w": 2, "x": 1}


def meets(path):
    return all(can(u, path, RIGHT[k]) == (u in who.split())
               for k, who in POLICY[path].items() for u in USERS)


total = 0
for path in sorted(FILES, key=len):  # parents first: a child's access needs them
    owner, group, old = FILES[path]
    good = []
    for mode in range(512):
        FILES[path] = (owner, group, mode)
        if meets(path):
            good.append(mode)
    new = min(good, key=lambda m: bin(m).count("1"))
    FILES[path] = (owner, group, new)
    changed = bin(old ^ new).count("1")
    total += changed
    print(f"{path:22} {old:o} -> {new:o}  ({len(good)} mode(s) fit,"
          f" {changed} bits changed)")
print("bits changed in all:", total)
