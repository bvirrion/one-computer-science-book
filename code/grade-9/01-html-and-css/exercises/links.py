from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from html_tree import name_of, tags  # noqa: E402


def links(text):
    """The address of every link (the href of every a element) of an HTML text."""
    found = []
    for tag in tags(text):
        if name_of(tag) == "a" and not tag.startswith("/"):
            start = tag.find('href="') + len('href="')
            found.append(tag[start:tag.find('"', start)])
    return found
