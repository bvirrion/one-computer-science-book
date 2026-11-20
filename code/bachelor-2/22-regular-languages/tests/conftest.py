import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
for sub in ("listings", "exercises", "figures"):
    sys.path.insert(0, str(HERE / sub))
