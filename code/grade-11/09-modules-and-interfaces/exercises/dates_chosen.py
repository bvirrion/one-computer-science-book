"""One interface, two implementations chosen at import (exercise 13).

The environment variable DATESET names the implementation: list or set (default).
"""
import os

if os.environ.get("DATESET", "set") == "list":
    from dateset_list import add, contains, empty, from_dates, size
else:
    from dateset_set import add, contains, empty, from_dates, size

__all__ = ["empty", "from_dates", "add", "contains", "size"]
