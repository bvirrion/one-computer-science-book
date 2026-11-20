"""timer.py -- a kernel in Python around the rv machine. A timer interrupt every 50
instructions saves the running process's registers and pc in its process control
block, picks the next ready process in turn, and restores its registers: preemption,
with no help from the programs. Each exit ecall ends only the process that makes it."""
from rv import Machine

QUANTUM = 50
m = Machine(open("two_loops.S").read())
pcbs = []  # process control blocks: name, saved pc, saved registers, still running?
for name in ("a", "b"):
    pc = m.prog.symbols[f"task_{name}"]
    regs = list(m.x)
    regs[2] = 0x7FFFFFF0 - 4096 * len(pcbs)  # sp: each process its own stack
    pcbs.append({"name": name, "pc": pc, "regs": regs, "alive": True})
running, switches = 0, 0


def exit_process(machine):  # ecall 10: this process is done, the machine goes on
    pcbs[running]["alive"] = False


m.ecalls[10] = exit_process
m.pc, m.x[:] = pcbs[0]["pc"], pcbs[0]["regs"]
since = 0
while any(p["alive"] for p in pcbs):
    m.step()
    since += 1
    if since == QUANTUM or not pcbs[running]["alive"]:  # timer, or the process ended
        pcbs[running]["pc"], pcbs[running]["regs"] = m.pc, list(m.x)  # save
        nxt = running
        for k in range(1, len(pcbs) + 1):  # round robin over the live processes
            if pcbs[(running + k) % len(pcbs)]["alive"]:
                nxt = (running + k) % len(pcbs)
                break
        if nxt != running:
            switches += 1
        running, since = nxt, 0
        m.pc, m.x[:] = pcbs[running]["pc"], pcbs[running]["regs"]  # restore
print("printed:", m.output_text)
print(f"{m.steps} instructions, {switches} switches")
