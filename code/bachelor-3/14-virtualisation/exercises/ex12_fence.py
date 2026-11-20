"""ex12_fence.py -- memory isolation by checking: before each guest load or store,
compute its address and stop the guest if it falls outside [lo, hi)."""
from rv import RVFault


def checked_step(m, lo, hi):
    found = m.instruction_at(m.pc)
    ins = found[0] if found else None
    memory = ("lb", "lh", "lw", "lbu", "lhu", "sb", "sh", "sw")
    if ins is not None and ins.mnemonic in memory:
        addr = (m.x[ins.rs1] + ins.imm) & 0xFFFFFFFF
        size = {"b": 1, "h": 2, "w": 4}[ins.mnemonic[1]]
        if not (lo <= addr and addr + size <= hi):
            raise RVFault(f"guest {ins.mnemonic} at 0x{addr:08x}: outside", m.pc)
    return m.step()

