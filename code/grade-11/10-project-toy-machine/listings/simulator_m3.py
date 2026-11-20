"""Milestone 3: the core of the simulator: fetch, decode, execute."""


def new_machine(memory, inputs=()):
    """A machine in its starting state, with the program in memory."""
    return {"mem": list(memory), "reg": [0, 0, 0, 0], "pc": 0, "sp": 0,
            "flags": {"Z": 0, "N": 0, "C": 0}, "inputs": list(inputs),
            "outputs": [], "halted": False, "steps": 0}


def halt(m, r, b):
    m["halted"] = True
    m["pc"] -= 2                     # PC stays on the HALT


def loadi(m, r, b):
    m["reg"][r] = b


def load(m, r, b):
    m["reg"][r] = m["mem"][b]


def store(m, r, b):
    m["mem"][b] = m["reg"][r]


def jmp(m, r, b):
    m["pc"] = b


def out(m, r, b):
    m["outputs"].append(m["reg"][r])


def nop(m, r, b):
    pass


EXECUTE = {0: halt, 1: loadi, 2: load, 3: store, 14: jmp, 20: out, 27: nop}


def step(m, execute=EXECUTE):
    """Run one instruction: fetch two bytes, decode them, execute."""
    if m["pc"] > 254:
        raise RuntimeError(f"PC = {m['pc']}: past the end of memory")
    b0, b1 = m["mem"][m["pc"]], m["mem"][m["pc"] + 1]          # fetch
    m["pc"] += 2
    m["steps"] += 1
    opcode, r = b0 // 4, b0 % 4                                 # decode
    if opcode not in execute:
        raise RuntimeError(f"no instruction has operation code {opcode}"
                           f" (address {m['pc'] - 2})")
    execute[opcode](m, r, b1)                                   # execute


def run(m, max_steps=10_000, execute=EXECUTE, trace=None):
    """Step until HALT; stop with an error after max_steps steps."""
    while not m["halted"]:
        if m["steps"] >= max_steps:
            raise RuntimeError(f"no HALT after {max_steps} steps")
        if trace:
            trace(m)
        step(m, execute)
    return m["outputs"]
