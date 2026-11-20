"""Who may read, write or enter each file of the school's server?"""
GROUPS = {"teachers": {"ana", "ben"}, "students": {"chloe", "dev"}}
USERS = ["ana", "ben", "chloe", "dev"]
FILES = {  # path: (owner, group, mode)
    "/school": ("ana", "teachers", 0o755),
    "/school/timetable.txt": ("ana", "teachers", 0o666),
    "/school/news.txt": ("ben", "teachers", 0o644),
    "/school/marks": ("ana", "teachers", 0o755),
    "/school/marks/g11.csv": ("ana", "teachers", 0o644),
    "/school/exam.txt": ("ben", "teachers", 0o644),
}


def bits(user, path):
    """The bits (r, w, x) that apply to this user: owner, else group, else others."""
    owner, group, mode = FILES[path]
    if user == owner:
        return (mode >> 6) & 7
    if user in GROUPS[group]:
        return (mode >> 3) & 7
    return mode & 7


def can(user, path, right):
    """right is 4 (read), 2 (write) or 1 (execute; for a directory, enter)."""
    parents = [p for p in FILES if path.startswith(p + "/")]
    return all(bits(user, p) & 1 for p in parents) and bool(bits(user, path) & right)


if __name__ == "__main__":
    print(f"{'':22}" + "".join(f"{u:>7}" for u in USERS))
    for path, (_, _, mode) in FILES.items():
        row = ""
        for u in USERS:
            r = "r" if can(u, path, 4) else "-"
            w = "w" if can(u, path, 2) else "-"
            row += f"{r + w:>7}"
        print(f"{path:22}{row}   {mode:o}")
