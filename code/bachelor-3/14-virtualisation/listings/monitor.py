"""monitor.py -- trap and emulate. The guest runs on the rv machine instruction by
instruction; every instruction the machine cannot run traps to this monitor, which
emulates it on virtual devices and resumes the guest after it."""
from rv import Machine, RVFault

CONSOLE, POWER, CLOCK, NUMBER = 0x5C0, 0x5C1, 0x5C2, 0x5C3


class Monitor:
    def __init__(self, source):
        self.m = Machine(source)
        self.m.on_trap = self.trap  # every illegal word, ecall and ebreak comes here
        self.console = []

    def read_csr(self, csr):
        if csr == CLOCK:
            return self.m.steps  # virtual time: the guest's instructions so far
        if csr in (CONSOLE, POWER, NUMBER):
            return 0
        raise RVFault(f"no device at CSR 0x{csr:03x}")

    def write_csr(self, csr, value):
        if csr == CONSOLE:
            self.console.append(chr(value & 0xFF))
        elif csr == NUMBER:
            self.console.append(f"{value}\n")
        elif csr == POWER:
            self.m.halt(value & 0xFF)
        elif csr != CLOCK:
            raise RVFault(f"no device at CSR 0x{csr:03x}")

    def trap(self, m, cause):
        word = m.load(m.pc, 4)  # the trapping instruction, fetched from the guest
        if cause != "illegal" or word & 0x7F != 0x73:  # not a CSR instruction
            raise RVFault(f"guest {cause} at 0x{m.pc:08x}: not emulated")
        funct3, rd, rs1 = word >> 12 & 7, word >> 7 & 31, word >> 15 & 31
        csr = word >> 20
        old = self.read_csr(csr)
        if funct3 == 1:  # csrrw: write rs1, old value to rd
            self.write_csr(csr, m.x[rs1])
        elif funct3 == 2 and rs1:  # csrrs: set rs1's bits (csrr has rs1 = x0)
            self.write_csr(csr, old | m.x[rs1])
        elif funct3 != 2:
            raise RVFault(f"CSR instruction 0x{word:08x} not emulated")
        if rd:
            m.set_reg(rd, old)
        m.pc += 4  # resume after the emulated instruction

    def run(self, max_steps=1_000_000):
        status = self.m.run(max_steps)
        return "".join(self.console), status
