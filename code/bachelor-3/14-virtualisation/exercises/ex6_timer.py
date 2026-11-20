"""ex6_timer.py -- a virtual timer device. The guest writes the address of its handler
to CSR 0x5c5 and a time to CSR 0x5c4; when the virtual clock reaches that time, the
monitor saves the guest's pc in CSR 0x5c6 and jumps to the handler. It fires once."""
from monitor import Monitor

TIMECMP, HANDLER, EPC = 0x5C4, 0x5C5, 0x5C6


class TimerMonitor(Monitor):
    def __init__(self, source):
        super().__init__(source)
        self.timer = {TIMECMP: 0, HANDLER: 0, EPC: 0}

    def read_csr(self, csr):
        return self.timer[csr] if csr in self.timer else super().read_csr(csr)

    def write_csr(self, csr, value):
        if csr in self.timer:
            self.timer[csr] = value
        else:
            super().write_csr(csr, value)

    def run(self, max_steps=1_000_000):
        m = self.m
        while not m.halted and m.steps < max_steps:
            if self.timer[TIMECMP] and m.steps >= self.timer[TIMECMP]:
                self.timer[EPC], m.pc = m.pc, self.timer[HANDLER]  # an interrupt
                self.timer[TIMECMP] = 0
            m.step()
        return "".join(self.console), m.exit_code
