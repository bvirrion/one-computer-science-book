"""Count the files under a folder, at any depth, on a tree built for the test."""
import tempfile
from pathlib import Path


def count_files(folder):
    total = 0
    for entry in folder.iterdir():
        if entry.is_dir():
            total += count_files(entry)      # a folder: count what it holds
        else:
            total += 1                       # a file: count it
    return total


TREE = ["school/notes.txt", "school/maths/ch1.txt", "school/maths/ch2.txt",
        "school/maths/old/ch0.txt", "photos/sea.jpg", "photos/2026/june/a.jpg",
        "photos/2026/june/b.jpg", "photos/2026/july/c.jpg", "todo.txt"]

with tempfile.TemporaryDirectory() as top:
    root = Path(top)
    for name in TREE:
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text("")
    print("files:", count_files(root))
    print("in photos:", count_files(root / "photos"))
    print("in school/maths:", count_files(root / "school" / "maths"))
