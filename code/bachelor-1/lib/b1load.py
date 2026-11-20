"""Import a chapter's listing or exercise module by path, from its tests.

    from b1load import load
    sieve = load(__file__, "pysieve")               # ../listings/pysieve.py
    sol = load(__file__, "topk", where="exercises")  # ../exercises/topk.py
"""
import importlib.util
import sys
from pathlib import Path


def load(test_file, name, where="listings"):
    path = Path(test_file).resolve().parent.parent / where / f"{name}.py"
    key = f"b1_{path.parent.parent.name}_{where}_{name}".replace("-", "_")
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(path.parent))
    return mod
