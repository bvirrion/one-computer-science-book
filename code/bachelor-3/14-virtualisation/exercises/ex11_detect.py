"""ex11_detect.py -- an honest clock gives the monitor away. ChargingMonitor adds the
monitor's own work, `charge` instructions per trap, to the guest's clock."""
from monitor import CLOCK, Monitor


class ChargingMonitor(Monitor):
    def __init__(self, source, charge):
        super().__init__(source)
        self.charge = charge

    def read_csr(self, csr):
        if csr == CLOCK:
            return self.m.steps + self.charge * (self.m.traps - 1)
        return super().read_csr(csr)


GUEST = """
main:   .word 0x5c2022f3        # csrr t0, 0x5c2: the clock
        .word 0x5c202373        # csrr t1, 0x5c2: the clock again, one instruction later
        sub   a0, t1, t0
        addi  a0, a0, -1        # anything above 1 instruction is the monitor's
        .word 0x5c351073        # csrw 0x5c3, a0: show it
        li    a0, 0
        .word 0x5c151073        # power off
"""
