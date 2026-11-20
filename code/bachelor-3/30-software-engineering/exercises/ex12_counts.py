"""Exercise 12: the coverage tool, extended to count how many times each line runs."""

from collections import Counter

from coverage_tool import Coverage


class LineCounts(Coverage):
    def __init__(self, path):
        super().__init__(path)
        self.counts = Counter()

    def _line(self, code, line):
        if self._ours(code):
            self.counts[line] += 1
            self.lines.add(line)
        # no DISABLE: every execution of the line must be reported
