"""Statement and branch coverage of one source file, measured with sys.monitoring
(Python 3.12 and later): the interpreter calls us at each new line and each branch."""

import dis
import itertools
import sys
from pathlib import Path

mon = sys.monitoring
TOOL = mon.COVERAGE_ID


def code_objects(code):
    yield code
    for const in code.co_consts:
        if hasattr(const, "co_code"):
            yield from code_objects(const)


def jumps(code):
    """The conditional jumps of one code object: {offset: (line, two destinations)}."""
    found = {}
    instructions = list(dis.get_instructions(code))
    following = {a.offset: b.offset for a, b in itertools.pairwise(instructions)}
    names = {i.offset: i.opname for i in instructions}
    for here in instructions:
        if here.opname.startswith("POP_JUMP_IF") or here.opname == "FOR_ITER":
            target = here.argval
            if names.get(target) == "END_FOR":  # a finished loop goes on after END_FOR
                target = following[target]
            found[here.offset] = (
                here.positions.lineno,
                {following[here.offset], target},
            )
    return found


class Coverage:
    def __init__(self, path):
        self.path = str(Path(path).resolve())
        top = compile(Path(path).read_text(), self.path, "exec")
        self.codes = list(code_objects(top))
        self.statements = {
            line
            for c in self.codes
            for _, _, line in c.co_lines()
            if line is not None and line > 0
        }
        self.statements -= {c.co_firstlineno for c in self.codes[1:]}  # def lines
        self.lines, self.arcs, self.seen = set(), set(), {}

    def _ours(self, code):
        if code.co_filename not in self.seen:
            self.seen[code.co_filename] = (
                str(Path(code.co_filename).resolve()) == self.path
            )
        return self.seen[code.co_filename]

    def _line(self, code, line):
        if self._ours(code):
            self.lines.add(line)
        return mon.DISABLE  # a line counts once: stop telling us about it

    def _branch(self, code, offset, destination):
        if self._ours(code):
            self.arcs.add((code.co_qualname, offset, destination))

    def __enter__(self):
        mon.use_tool_id(TOOL, "book-coverage")
        mon.register_callback(TOOL, mon.events.LINE, self._line)
        mon.register_callback(TOOL, mon.events.BRANCH, self._branch)
        mon.set_events(TOOL, mon.events.LINE | mon.events.BRANCH)
        return self

    def __exit__(self, *exc):
        mon.set_events(TOOL, mon.events.NO_EVENTS)
        mon.free_tool_id(TOOL)
        mon.restart_events()  # re-enable what DISABLE switched off, for the next run

    def report(self):
        run = self.statements & self.lines
        branches, missed = 0, []
        for code in self.codes:
            for offset, (line, destinations) in jumps(code).items():
                for d in sorted(destinations):
                    branches += 1
                    if (code.co_qualname, offset, d) not in self.arcs:
                        missed.append(line)
        return {
            "statements": (len(run), len(self.statements)),
            "missed lines": sorted(self.statements - self.lines),
            "branches": (branches - len(missed), branches),
            "missed branches at lines": sorted(missed),
        }
