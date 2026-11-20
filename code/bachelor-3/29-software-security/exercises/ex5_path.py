"""Exercise 5: the toy app's file route serves files from a public folder by name.
The buggy version joins the name to the folder, so "../" climbs out of it; the fixed
version resolves the path and refuses anything outside the folder."""

from pathlib import Path


def serve_buggy(public, name):
    return (Path(public) / name).read_text()


def serve_fixed(public, name):
    root = Path(public).resolve()
    target = (root / name).resolve()  # follows "..", and symbolic links
    if not target.is_relative_to(root) or not target.is_file():
        raise PermissionError(f"refused: {name}")
    return target.read_text()
