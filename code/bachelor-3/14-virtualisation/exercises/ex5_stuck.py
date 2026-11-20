"""ex5_stuck.py -- a monitor that emulates the instruction, then forgets to step
over it."""
from monitor import Monitor


class StuckMonitor(Monitor):
    def trap(self, m, cause):
        pc = m.pc
        super().trap(m, cause)
        m.pc = pc  # the bug, made explicit: the guest resumes at the same instruction
