"""A program reading a program: Python's ast module parses euclid.py."""
import ast
from pathlib import Path

source = Path("euclid.py").read_text()
tree = ast.parse(source)                         # the text becomes a tree
kinds = {}
for node in ast.walk(tree):
    name = type(node).__name__
    kinds[name] = kinds.get(name, 0) + 1
print(len(source), "characters,", len(source.splitlines()), "lines")
print("functions:", [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
print("while loops:", kinds.get("While", 0), "  for loops:", kinds.get("For", 0),
      "  calls:", kinds.get("Call", 0))
