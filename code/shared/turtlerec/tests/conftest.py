# tools/test_code.sh does not put code/shared/turtlerec on PYTHONPATH: add it here.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
